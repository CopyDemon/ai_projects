import { useEffect, useRef, useState } from 'react'
import './Camera.css'

// 摄像头组件：开摄像头、每隔几秒拍一张、把照片交给外面。
// 外面通过 onFrame 拿到每张照片的 blob。现在 App 没传 onFrame，照片只显示在页面上。
export default function Camera({ onFrame }) {
  // ref 是拿来存"不影响画面"的东西：真实的 DOM 元素、视频流
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)

  // state 是拿来存"一变画面就要跟着变"的东西
  const [running, setRunning] = useState(false)
  const [seconds, setSeconds] = useState(3)
  const [count, setCount] = useState(0)
  const [last, setLast] = useState(null)
  const [error, setError] = useState('')

  async function openCamera() {
    // 浏览器只在 https 或 localhost 下才有 navigator.mediaDevices
    if (!navigator.mediaDevices) {
      throw new Error('这个浏览器或这个网址不允许开摄像头。要用 https 或 localhost 打开')
    }
    // facingMode environment 是手机的后置摄像头，电脑上没有就用默认的
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment', width: { ideal: 640 } },
      audio: false,
    })
    streamRef.current = stream
    const video = videoRef.current
    video.srcObject = stream
    await new Promise((resolve) => (video.onloadedmetadata = resolve))
  }

  async function start() {
    if (streamRef.current) return
    try {
      await openCamera()
      setError('')
      setRunning(true)
    } catch (e) {
      setError('开摄像头失败：' + e.message)
    }
  }

  function stop() {
    setRunning(false)
    streamRef.current?.getTracks().forEach((t) => t.stop())
    streamRef.current = null
    if (videoRef.current) videoRef.current.srcObject = null
  }

  // running 变成 true 就开定时器。running 变 false、间隔改了、或组件被拆掉时，清掉旧定时器
  useEffect(() => {
    if (!running) return

    function takeFrame() {
      const video = videoRef.current
      const canvas = canvasRef.current
      if (!video || !canvas || !video.videoWidth) return
      // 把视频当前这一帧画到 canvas 上，再转成 jpeg
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      canvas.getContext('2d').drawImage(video, 0, 0)
      canvas.toBlob(
        (blob) => {
          setCount((c) => c + 1)
          setLast((prev) => {
            if (prev) URL.revokeObjectURL(prev.url)
            return {
              url: URL.createObjectURL(blob),
              time: new Date().toLocaleTimeString(),
              width: canvas.width,
              height: canvas.height,
              kb: Math.round(blob.size / 1024),
            }
          })
          onFrame?.(blob)
        },
        'image/jpeg',
        0.8,
      )
    }

    takeFrame()
    const timer = setInterval(takeFrame, Math.max(1, seconds) * 1000)
    return () => clearInterval(timer)
  }, [running, seconds, onFrame])

  // 拍的张数变了就更新标签页标题
  useEffect(() => {
    document.title = count ? `Snake Eye 已拍 ${count} 张` : 'Snake Eye'
  }, [count])

  // 网址后面加 ?auto=1 就自动开始，便携设备开机打开网页就一直看。
  // 组件被拆掉时只需要关掉摄像头流，不用改 state，页面都没了
  useEffect(() => {
    if (new URLSearchParams(location.search).get('auto') === '1') {
      openCamera().then(
        () => setRunning(true),
        (e) => setError('开摄像头失败：' + e.message),
      )
    }
    return () => {
      streamRef.current?.getTracks().forEach((t) => t.stop())
      streamRef.current = null
    }
  }, [])

  let status = '还没开始'
  if (running && !last) status = '摄像头开了，正在看'
  if (last) status = `已拍 ${count} 张，最近一张 ${last.time}，${last.width}x${last.height}，${last.kb} KB`
  if (!running && count) status = `停了，一共拍了 ${count} 张`

  return (
    <div className="camera">
      <div className="label">摄像头实时画面</div>
      <video ref={videoRef} autoPlay playsInline muted />

      <div className="row">
        <button onClick={start} disabled={running}>开始看</button>
        <button onClick={stop} disabled={!running}>停止</button>
        每隔{' '}
        <input
          type="number"
          min="1"
          value={seconds}
          onChange={(e) => setSeconds(Number(e.target.value) || 1)}
        />{' '}
        秒拍一张
      </div>

      <div className="status">{status}</div>
      {error && <div className="error">{error}</div>}

      <div className="label">最近拍到的一张</div>
      {last && <img src={last.url} alt="" />}

      <canvas ref={canvasRef} hidden />
    </div>
  )
}
