import Camera from './components/Camera.jsx'

// 整个页面就一个摄像头组件。
// 第四步连后端时，在这里给 Camera 传一个 onFrame 函数，把每张照片 POST 给服务器。
export default function App() {
  return (
    <>
      <h1>🐍 Snake Eye 前端</h1>
      <Camera />
    </>
  )
}
