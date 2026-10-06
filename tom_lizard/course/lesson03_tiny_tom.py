"""第三课：从零训练一个 1KB 的小 Tom，教它认识 1 2 3 4 5

运行方法：
    conda activate tom_lizard
    cd tom_lizard/course
    python lesson03_tiny_tom.py

训练的数学参考斯坦福 CS231n 的讲义 https://cs231n.github.io/neural-networks-case-study/
"""

from pathlib import Path

import numpy as np

rng = np.random.default_rng(42)

# ============================================================
# 第一步：准备教材
# 每个数字画在 5 列 7 行的小格子里，# 是黑点，. 是白点。
# 这就是 Tom 能看到的全部东西：35 个点，每个点是 0 或 1。
# ============================================================

DIGITS = {
    1: """
..#..
.##..
..#..
..#..
..#..
..#..
.###.""",
    2: """
.###.
#...#
....#
...#.
..#..
.#...
#####""",
    3: """
.###.
#...#
....#
..##.
....#
#...#
.###.""",
    4: """
...#.
..##.
.#.#.
#..#.
#####
...#.
...#.""",
    5: """
#####
#....
####.
....#
....#
#...#
.###.""",
}

# 一个 Tom 从来没学过的数字，最后拿来考它
SIX = """
.###.
#....
#....
####.
#...#
#...#
.###."""


def to_pixels(drawing: str) -> np.ndarray:
    """把画出来的数字变成 35 个 0 和 1"""
    rows = drawing.strip().splitlines()
    return np.array([1.0 if ch == "#" else 0.0 for row in rows for ch in row])


def show(pixels: np.ndarray) -> str:
    """把 35 个数字画回格子，方便人看"""
    grid = pixels.reshape(7, 5)
    return "\n".join("".join("█" if v > 0.5 else "·" for v in row) for row in grid)


def add_noise(pixels: np.ndarray, flip_rate: float) -> np.ndarray:
    """随机把一些点黑白反过来，模拟写得歪歪扭扭的字"""
    flip = rng.random(pixels.shape) < flip_rate
    return np.where(flip, 1.0 - pixels, pixels)


def make_dataset(per_digit: int, flip_rate: float):
    """每个数字做 per_digit 份带噪点的样本"""
    X, y = [], []
    for digit, drawing in DIGITS.items():
        clean = to_pixels(drawing)
        for _ in range(per_digit):
            X.append(add_noise(clean, flip_rate))
            y.append(digit - 1)  # 答案存成 0 到 4，因为程序里数位置是从 0 开始的
    return np.array(X), np.array(y)


# 训练用的课本和考试用的卷子分开，考试题 Tom 学的时候没见过
X_train, y_train = make_dataset(per_digit=200, flip_rate=0.1)
X_test, y_test = make_dataset(per_digit=100, flip_rate=0.1)

# ============================================================
# 第二步：造一个什么都不会的大脑
# 大脑就是一堆数字，叫参数。一开始全是随机的，所以 Tom 什么都不会。
#
#   35 个点  →  6 个中间神经元  →  5 个输出，分别代表 1 2 3 4 5
#
# W1 是第一层的连线强度，35 × 6 个数字
# b1 是第一层每个神经元自己的偏好，6 个数字
# W2 是第二层的连线强度，6 × 5 个数字
# b2 是第二层的偏好，5 个数字
# ============================================================

INPUTS, HIDDEN, OUTPUTS = 35, 6, 5
W1 = rng.normal(0, np.sqrt(2 / INPUTS), (INPUTS, HIDDEN))
b1 = np.zeros(HIDDEN)
W2 = rng.normal(0, np.sqrt(2 / HIDDEN), (HIDDEN, OUTPUTS))
b2 = np.zeros(OUTPUTS)

n_params = W1.size + b1.size + W2.size + b2.size
print(f"Tom 的大脑一共有 {n_params} 个参数，每个用 4 个字节存，总共 {n_params * 4} 字节，大约 1KB\n")


def think(X):
    """Tom 看到图，算出对 1 到 5 各有几成把握"""
    hidden = np.maximum(0, X @ W1 + b1)  # 中间层。负数变 0，这个叫 ReLU
    scores = hidden @ W2 + b2  # 每个数字一个分数
    # softmax：把分数变成加起来等于 1 的概率
    exp = np.exp(scores - scores.max(axis=1, keepdims=True))
    probs = exp / exp.sum(axis=1, keepdims=True)
    return hidden, probs


def exam(X, y):
    """考试，返回正确率"""
    _, probs = think(X)
    return (probs.argmax(axis=1) == y).mean()


def ask(pixels, title):
    """给 Tom 看一张图，打印它的回答"""
    _, probs = think(pixels[None, :])
    probs = probs[0]
    print(title)
    print(show(pixels))
    guesses = "  ".join(f"{d + 1}:{p:4.0%}" for d, p in enumerate(probs))
    print(f"Tom 觉得：{guesses}  →  它说是 {probs.argmax() + 1}\n")


# ============================================================
# 第三步：训练前先考一次
# ============================================================

print("======== 训练前 ========\n")
print(f"考试正确率：{exam(X_test, y_test):.0%}，五选一瞎猜大概是 20%\n")
sample = add_noise(to_pixels(DIGITS[3]), 0.1)
ask(sample, "给 Tom 看一个带噪点的 3：")

# ============================================================
# 第四步：训练
# 一遍一遍重复这四件事：
#   1. 猜：让 Tom 看一批图，给出答案
#   2. 对答案：看它离正确答案差多少，这个差距叫 loss
#   3. 找方向：算出每个参数往哪边调能让 loss 变小，这叫反向传播
#   4. 调一点点：每个参数朝那个方向挪一小步，步子大小叫学习率
# ============================================================

LEARNING_RATE = 0.5
ROUNDS = 10
BATCH = 50  # 一次看 50 张图再调参数，这一小批叫 batch
N = len(X_train)
REPORT_AT = {1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 50, 100, 200}

print("======== 开始训练 ========\n")
print(f"课本一共 {N} 张图，每次看 {BATCH} 张调一次，看完一遍课本叫一轮，一共学 {ROUNDS} 轮\n")
step = 0
for rnd in range(1, ROUNDS + 1):
    order = rng.permutation(N)  # 每轮打乱顺序，免得 Tom 背顺序
    for start in range(0, N, BATCH):
        idx = order[start : start + BATCH]
        X, y = X_train[idx], y_train[idx]

        # 1. 猜
        hidden, probs = think(X)

        # 2. 对答案。loss 是正确答案那一项概率的负对数，越接近 100% loss 越接近 0
        loss = -np.log(probs[np.arange(len(y)), y]).mean()

        # 3. 找方向，跟 CS231n 讲义里的写法一样
        dscores = probs.copy()
        dscores[np.arange(len(y)), y] -= 1
        dscores /= len(y)
        dW2 = hidden.T @ dscores
        db2 = dscores.sum(axis=0)
        dhidden = dscores @ W2.T
        dhidden[hidden <= 0] = 0
        dW1 = X.T @ dhidden
        db1 = dhidden.sum(axis=0)

        # 4. 每个参数往让 loss 变小的方向挪一小步
        W1 -= LEARNING_RATE * dW1
        b1 -= LEARNING_RATE * db1
        W2 -= LEARNING_RATE * dW2
        b2 -= LEARNING_RATE * db2

        step += 1
        if step in REPORT_AT:
            print(f"第 {rnd:2d} 轮  第 {step:3d} 次调整  loss {loss:.3f}  考试正确率 {exam(X_test, y_test):.1%}")

# ============================================================
# 第五步：训练后再考
# ============================================================

print("\n======== 训练后 ========\n")
ask(sample, "还是刚才那个带噪点的 3：")
for flip_rate in (0.0, 0.1, 0.2, 0.3):
    Xn, yn = make_dataset(per_digit=200, flip_rate=flip_rate)
    print(f"噪点 {flip_rate:.0%} 的卷子，正确率 {exam(Xn, yn):.1%}")
print()

# 第六步：考一个从来没学过的数字
ask(to_pixels(SIX), "给 Tom 看一个它从来没学过的 6：")

# 第七步：把 Tom 的大脑存成文件，看看到底多大
brain = np.concatenate([W1.ravel(), b1, W2.ravel(), b2]).astype(np.float32)
path = Path(__file__).parent / "tiny_tom_brain.bin"
brain.tofile(path)
print(f"Tom 的大脑存到了 {path.name}，文件大小 {path.stat().st_size} 字节")
