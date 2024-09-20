在传统的衍生品合约中，一般存在固定到期日(Maturity): $T$。但是对于一些特定的新兴的衍生品合约，比如Uniswap V3，可以不存在一个固定到期日，也就是说合约的到期日完全依赖权利方行权或提前约定的停时。对于这种衍生品合约的定价问题，计算停时的Laplace 变换是一个常用的手段，本文意在给出带有drift的布朗运动双边吸收壁停时的Laplace变换。
## 0. Definition

对于一个Markov随机过程$X(t)$, 定义状态转移概率 $P(x|y,t)$
$$
P(x|y,t) = \text{Pr}(X(t+s)<y|X(s)=x)
$$
由Markov性质可以得到Chapman-Kolmogorov Equation:
$$
P(x|y,t_1+t_2)= \int_{-\infty}^{\infty}P(z|y,t_1)d_z P(x|z,t_2)
$$
定义双边吸收壁停时$\tau_{ab}$
$$
\tau_{ab}(x) = \sup\{t|a<X(s)<b, 0\leq s \leq t\}
$$
假设$\tau_{ab}$ 的累计分布函数：
$$
F_{ab}(x|t) = \text{Pr}(\tau_{ab}(x)<t)
$$
我们预设$P(x|y,t)$ 和 $F_{ab}(x|t)$ 的一阶导数存在：
$$
\begin{aligned}
p(x|y,t) &= \frac{\partial}{\partial y}P(x|y,t)\\
f_{ab}(x|t) &= \frac{\partial}{\partial t}F_{ab}(x|t)
\end{aligned}
$$
其中$f_{ab}(x|t)$ 是停时的概率密度函数。
对于单边吸收壁停时情况：
$$
\tau_c(x)=\left\{
\begin{aligned}
\tau_{c,\infty}(x) & & \text{if}  x>c \\
\tau_{-\infty,c}(x) & & \text{if}  x\leq c
\end{aligned}
\right.
$$
相应的单边吸收壁停时也有对应的累计分布函数和概率密度函数：
$$
\begin{aligned}
F_{c}(x|t) &= \text{Pr}(\tau_{ab}(x)<t) < 1\\
f_{c}(x|t) &= \frac{\partial}{\partial t}F_{c}(x|t)
\end{aligned}
$$
进而，我们可以定义双边情境下两个$b$ 和$a$ 两个吸收壁分别的累计密度函数：
$$
\begin{aligned}
F^{+}_{ab}(x|t) &= \text{Pr}(\tau_{ab}(x)<t, \tau_{ab} = \tau_{b})\\
F^{-}_{ab}(x|t) &= \text{Pr}(\tau_{ab}(x)<t, \tau_{ab} = \tau_{a})
\end{aligned}
$$
显然地:
$$
F_{ab}(x|t) = F^{+}_{ab}(x|t)+F^{-}_{ab}(x|t)
$$
对应地，
$$
\begin{aligned}
f^{+}_{ab}(x|t) &= \frac{\partial}{\partial t}F^{+}_{ab}(x|t)\\
f^{-}_{ab}(x|t) &= \frac{\partial}{\partial t}F^{-}_{ab}(x|t)
\end{aligned}
$$
对于任意的$p$ 和 $f$ , 定义它们的Laplace Transform
$$
\begin{aligned}
\hat p(x|y,\lambda) &= \int_0^{\infty}e^{-\lambda t}p(x|y,t)dt \\
\hat f^{+}_{ab}(x|\lambda) &= \int_0^{\infty}e^{-\lambda t}f^{+}_{ab}(x|t)dt 
\end{aligned}
$$


# 1. Optimal Stopping Theorem

 对于一个带有正漂移项$\mu >0$的布朗运动，$X(t) = \mu t+\sigma B_t$
$$
 假设单边吸收壁：
 $$ \tau(x)=\left\{
\begin{aligned}
\tau_{c,\infty}(x) & & \text{if}  x>c \\
\tau_{-\infty,c}(x) & & \text{if}  x\leq c
\end{aligned}
\right.
$$

 通过Wald's Identities 可以得知对于$\alpha >0$：
$$
M_t:=\exp \left(\alpha X_t-\alpha \mu t-\frac{1}{2} \alpha^2 t\right)
$$
是一个鞅。
所以由Optimal Stopping Theorem和DCT可知
$$\mathbb E(M_t)=1$$
由$X_\tau = c$ 可得：
$$
M_\tau=e^{\alpha c} \exp \left(-\left[\mu \alpha+\frac{1}{2} \alpha^2\right] \tau\right)
$$$$
\mathbb{E} [\exp \left(-\left[\mu \alpha+\frac{1}{2} \alpha^2\right] \tau\right)]=e^{-\alpha c}
$$
令$\lambda:=\mu \alpha+\frac{1}{2} \alpha^2$, 即
$$\alpha = -\mu \pm \sqrt{\mu^2 + 2\lambda}$$
所以单边拉普拉斯变换
$$
\mathbb E(e^{-\lambda \tau})=\exp[(\mu \mp \sqrt{\mu^2+2\lambda})c]
$$

# 2. CKE

由CKE可知, 对于$y>c>x$:
$$
p(x \mid y, t)=\int_0^t f_c(x \mid \tau) p(c \mid y, t-\tau) d \tau
$$
Laplace Transform:
$$
\hat{p}(x \mid y, \lambda)=\hat{f}_c(x \mid \lambda) \hat{p}(c \mid y, \lambda)
$$
所以
$$
\hat{f}_c(x \mid \lambda)= \frac{\hat{p}(x \mid y, \lambda)}{\hat{p}(c \mid y, \lambda)}
$$
也就是说：
$$
\hat{f}_c(x \mid \lambda)= \begin{cases}\frac{u(x)}{u(c)}, & x<c \\ \frac{v(x)}{v(c)}, & x>c .\end{cases}
$$

由上一节的结论可知
$$
\mathbb E(e^{-\lambda \tau})=\begin{cases}\exp[(\mu -\sqrt{\mu^2+2\lambda})(c-x)], & x<c \\ \exp[(\mu +\sqrt{\mu^2+2\lambda})(c-x)], & x>c .\end{cases}
$$
所以对于带有drift的布朗运动：
$$
\begin{aligned}
u(x) = \exp[(\mu -\sqrt{\mu^2+2\lambda})(-x)]\\
v(x) = \exp[(\mu +\sqrt{\mu^2+2\lambda})(-x)]
\end{aligned}
$$

对于双边吸收壁的情况：
$$
\begin{aligned}
& f_b(x \mid t)=f_{a b}^{+}(x \mid t)+\int_0^t f_{a b}^{-}(x \mid \tau) f_b(a \mid t-\tau) d \tau \\
& f_a(x \mid t)=f_{a b}^{-}(x \mid t)+\int_0^t f_{a b}^{+}(x \mid \tau) f_a(b\mid t-\tau) d \tau
\end{aligned}
$$

Laplace Transform:
$$
\begin{aligned}
& \hat{f}_b(x \mid \lambda)=\hat{f}_{a b}^{+}(x \mid \lambda)+\hat{f}_{a b}^{-}(x \mid \lambda) \hat{f}_b(a \mid \lambda) \\
& \hat{f}_a(x \mid \lambda)=\hat{f}_{a b}^{-}(x \mid \lambda)+\hat{f}_{a b}^{+}(x \mid \lambda) \hat{f}_a(b \mid \lambda)
\end{aligned}
$$
有两个线性方程两个未知数：

$$
\begin{aligned}
& \hat{f}_b(x \mid \lambda)-\frac{\hat{f}_a(x \mid \lambda)}{\hat{f}_a(b \mid \lambda)}=\hat{f}_{a b}^{-}(x \mid \lambda) [\hat{f}_b(a \mid \lambda)-\frac{1}{\hat{f}_a(b \mid \lambda)}] \\
& \hat{f}_a(x \mid \lambda)-\frac{\hat{f}_b(x \mid \lambda)}{\hat{f}_b(a \mid \lambda)}=\hat{f}_{a b}^{+}(x \mid \lambda) [\hat{f}_a(b \mid \lambda)-\frac{1}{\hat{f}_b(a \mid \lambda)}]
\end{aligned}
$$
代入$u(x),v(x)$得到：
$$
\begin{aligned}
\frac{u(x)}{u(b)}-\frac{v(x)}{v(b)}=\hat{f}_{a b}^{-}(x \mid \lambda)[\frac{u(a)}{u(b)}-\frac{v(a)}{v(b)}]\\
\frac{v(x)}{v(a)}-\frac{u(x)}{u(a)}=\hat{f}_{a b}^{-}(x \mid \lambda)[\frac{v(b)}{v(a)}-\frac{u(b)}{u(a)}]
\end{aligned}
$$
解方程得到
$$
\begin{aligned}
& \hat{f}_{a b}^{-}(x \mid \lambda)=\frac{v(b) u(x)-u(b) v(x)}{u(a) v(b)-u(b) v(a)} \\
& \hat{f}_{a b}^{+}(x \mid \lambda)=\frac{u(a) v(x)-v(a) u(x)}{u(a) v(b)-u(b) v(a)} \\
& \hat{f}_{a b}(x \mid \lambda)=\frac{v(x)(u(a)-u(b))-u(x)(v(a)-v(b))}{u(a) v(b)-u(b) v(a)}
\end{aligned}
$$

把$u(x),v(x)$的原式带入：

$$
\begin{aligned}
\hat{f}_{a b}^{-}(x \mid \lambda)&=\frac{v(b) u(x)-u(b) v(x)}{u(a) v(b)-u(b) v(a)}\\
&= \frac{\exp[(\mu +\sqrt{\mu^2+2\lambda})(-b)]\exp[(\mu -\sqrt{\mu^2+2\lambda})(-x)]-\exp[(\mu -\sqrt{\mu^2+2\lambda})(-b)]\exp[(\mu +\sqrt{\mu^2+2\lambda})(-x)]}{\exp[(\mu +\sqrt{\mu^2+2\lambda})(-b)] \exp[(\mu -\sqrt{\mu^2+2\lambda})(-a)]-\exp[(\mu -\sqrt{\mu^2+2\lambda})(-b)]\exp[(\mu +\sqrt{\mu^2+2\lambda})(-a)]}\\
&=\frac{\exp\{-[\mu(b+x)+\sqrt{\mu^2+2\lambda}(b-x)]\}-\exp\{-[\mu(b+x)+\sqrt{\mu^2+2\lambda}(x-b)]\}}{\exp\{-[\mu(b+a)+\sqrt{\mu^2+2\lambda}(b-a)]\}-\exp\{-[\mu(b+a)+\sqrt{\mu^2+2\lambda}(a-b)]\}}\\
&=\frac{\exp\{-[\mu(b+x)\}}{\exp\{-[\mu(b+a)\}} \frac{\sinh[(b-x)\sqrt{\mu^2+2\lambda}]}{\sinh[(b-a)\sqrt{\mu^2+2\lambda}]}\\
&= \exp[{\mu(a-x)}]\frac{\sinh[(b-x)\sqrt{\mu^2+2\lambda}]}{\sinh[(b-a)\sqrt{\mu^2+2\lambda}]}
\end{aligned}
$$

$$
\begin{aligned}
\hat{f}_{a b}^{+}(x \mid \lambda)&=\frac{u(a) v(x)-v(a) u(x)}{u(a) v(b)-u(b) v(a)}\\
&= \frac{\exp[(\mu -\sqrt{\mu^2+2\lambda})(-a)]\exp[(\mu +\sqrt{\mu^2+2\lambda})(-x)]-\exp[(\mu+-\sqrt{\mu^2+2\lambda})(-a)]\exp[(\mu -\sqrt{\mu^2+2\lambda})(-x)]}{\exp[(\mu +\sqrt{\mu^2+2\lambda})(-b)] \exp[(\mu -\sqrt{\mu^2+2\lambda})(-a)]-\exp[(\mu -\sqrt{\mu^2+2\lambda})(-b)]\exp[(\mu +\sqrt{\mu^2+2\lambda})(-a)]}\\
&=\frac{\exp\{-[\mu(a+x)+\sqrt{\mu^2+2\lambda}(x-a)]\}-\exp\{-[\mu(a+x)+\sqrt{\mu^2+2\lambda}(a-x)]\}}{\exp\{-[\mu(b+a)+\sqrt{\mu^2+2\lambda}(b-a)]\}-\exp\{-[\mu(b+a)+\sqrt{\mu^2+2\lambda}(a-b)]\}}\\
&=\frac{\exp\{-[\mu(a+x)\}}{\exp\{-[\mu(b+a)\}} \frac{\sinh[(x-a)\sqrt{\mu^2+2\lambda}]}{\sinh[(b-a)\sqrt{\mu^2+2\lambda}]}\\
&= \exp[{\mu(b-x)}]\frac{\sinh[(x-a)\sqrt{\mu^2+2\lambda}]}{\sinh[(b-a)\sqrt{\mu^2+2\lambda}]}
\end{aligned}
$$

