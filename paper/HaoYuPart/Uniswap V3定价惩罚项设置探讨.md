# Uniswap V3定价惩罚项设置探讨

我们注意到，在对于Uniswap V3的实际定价中，有些必定会存在的成本被我们给假设忽略掉了。比如

1. 在建仓/平仓的时候，我们会需要将手上的一部分钱兑换成ETH/手上的ETH换回现金，兑换过程需要支付手续费
2. 在平仓的时候，我们需要将手上的ETH换回现金，此时需要支付滑点成本

需要注意的是，平仓时候的手续费，在定价的时候是要计算折现的。

接下来，我们分部分计算

注：滑点成本暂不计算

## 建仓时候需要兑换的ETH所需要支付的手续费

根据V3的机制，我们在V3头寸建仓的时候，手上的资金池会有一部分兑换成ETH，这个过程是要实际发生ETH交易的，所以这个过程中会固定发生手续费，手续费率我们设为$C$（暂定，区别于定价公式的C），接下来我们需要计算，建仓的时候，需要兑换多少ETH。

我们注意到Uni V3的几个基本假设：

我们首先做出几个假设：
$$
\begin{align}
&1.进入的头寸的范围是(S_L,S_H)，此时的ETH价格是S_0 \\
&2.用于投资这个头寸的USDT总值是C \\
&3.进入头寸后，这笔总值为C的USDT自动转换为一部分ETH和一部分USDT，数量分别为x_0,y_0 \\
&4.退出头寸时，ETH和USDT的数量分别为x_T,y_T，此时ETH价格是S_T \\
\end{align}
$$
则存在以下几个基本假设(根据UniswapV3自身的定义与机制)：
$$
\begin{align}
&1.(x_0+\sqrt{\frac{K}{S_H}})(y_0+\sqrt{KS_L})=K=(x_T+\sqrt{\frac{K}{S_H}})(y_T+\sqrt{KS_L}) \\
&2.\frac{y_0+\sqrt{KS_L}}{x_0+\sqrt{\frac{K}{S_H}}}=S_0,\frac{y_T+\sqrt{KS_L}}{x_T+\sqrt{\frac{K}{S_H}}}=S_T \\
&3.S_0x_0+y_0=C \\
\end{align}
$$
本节需要求的ETH总价值就是$S_0x_0$，则存在：
$$
Target\ ETH \ Value=S_0x_0=\frac{CS_0}{2\sqrt{S_0}-\sqrt{S_L}-\frac{S_0}{\sqrt{S_H}}}(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}})
$$

这里的$Target\ ETH\ Value$需要根据我们的payoff公式做适配

由于我们的payoff公式形式为：

同时，基于标的价格的浮动，Uniswap V3的仓位价值也随之改变，V3仓位价值的计算公式如下：
$$
LP=
\begin{cases}
\lambda*S(\frac{1}{\sqrt{L}}-\frac{1}{\sqrt{H}}), S<L \\
\lambda*(2\sqrt{S}-\sqrt{L}-\frac{S}{\sqrt{H}}), L<S<H \\
\lambda*(\sqrt{H}-\sqrt{L}), H<S
\end{cases} \\
\lambda=\frac{1}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}
$$
我们可以看到，当payoff公式中的S=1时，LP=1，即代表着，在payoff公式的情形下，期初$S=\frac{S_0}{S_0}=1,LP=1=C$

所以：
$$
\begin{align}
Target\ ETH \ Value
&=S_0x_0 \\
&=\frac{CS_0}{2\sqrt{S_0}-\sqrt{S_L}-\frac{S_0}{\sqrt{S_H}}}(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}}) \\
&=\sqrt{S_0}\frac{C}{2\sqrt{S_0}-\sqrt{S_L}-\frac{S_0}{\sqrt{S_H}}}*\sqrt{S_0}(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}}) \\
&=\frac{C}{\frac{2\sqrt{S_0}-\sqrt{S_L}-\frac{S_0}{\sqrt{S_H}}}{\sqrt{S_0}}}(1-\frac{1}{\frac{\sqrt{S_H}}{\sqrt{S_0}}}) \\
&=\frac{1}{2-\sqrt{L}-\frac{1}{\sqrt{\frac{S_H}{S_0}}}}(1-\frac{1}{\sqrt{H}}) \\
&=\frac{1}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}(1-\frac{1}{\sqrt{H}})
\end{align}
$$
请注意，这是期初的经过归一化之后的需要兑换的ETH的总价值。期初减仓的手续费用应当是这个总价值乘以一个固定系数。

## 平仓时候需要兑换的ETH所需要支付的手续费

假设平仓时候的价格为$S_T$，则存在$Target\ ETH\ Value_{Ending}=S_Tx_T$

通过上一节的假设部分，我们很容易就能求出：
$$
x_T=\sqrt{K}(\frac{1}{\sqrt{S_T}}-\frac{1}{\sqrt{S_H}})
$$
而K保持着一个关系
$$
(x_0+\sqrt{\frac{K}{S_H}})(y_0+\sqrt{KS_L})=K=(x_T+\sqrt{\frac{K}{S_H}})(y_T+\sqrt{KS_L})
$$
所以K是期初就决定好的，根据推导：
$$
\sqrt{K}=\frac{C}{S_0(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}})+\sqrt{S_0}-\sqrt{S_L}}
$$
所以存在：
$$
\begin{align}
Target\ ETH \ Value_{Ending}
&=S_Tx_T \\
&=S_T\sqrt{K}(\frac{1}{\sqrt{S_T}}-\frac{1}{\sqrt{S_H}}) \\
&=S_T(\frac{1}{\sqrt{S_T}}-\frac{1}{\sqrt{S_H}})\frac{C}{S_0(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}})+\sqrt{S_0}-\sqrt{S_L}} \\
&=\frac{S_T}{S_0}\sqrt{S_0}(\frac{1}{\sqrt{S_T}}-\frac{1}{\sqrt{S_H}})\frac{C\sqrt{S_0}}{S_0(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}})+\sqrt{S_0}-\sqrt{S_L}} \\
&=s_t(\frac{1}{\sqrt{s_t}}-\frac{1}{\sqrt{H}})\frac{1}{\sqrt{S_0}(\frac{1}{\sqrt{S_0}}-\frac{1}{\sqrt{S_H}})+1-\sqrt{L}} \\
&=s_t(\frac{1}{\sqrt{s_t}}-\frac{1}{\sqrt{H}})\frac{1}{(1-\frac{1}{\sqrt{H}})+1-\sqrt{L}} \\
&=s_t(\frac{1}{\sqrt{s_t}}-\frac{1}{\sqrt{H}})\frac{1}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}
\end{align}
$$
其中：$s_t=\frac{S_T}{S_0}$

## 总结

所以平仓时候需要交易的ETH的价值得证，注意在定价过程中，平仓时候的手续费=平仓时候交易的ETH价值\*手续费系数\*相应的价值贴现。由此我们分以下四种情况来论述：（一些用语承接自之前的定价研究）。我们假设所有的手续费收取按照固定的手续费系数k做代表

### 1.当运动为0drift布朗运动，且为欧式定价的时候，由于欧式定价的平仓时机只有两种价格状态$[L,H]$，其中H状态时持有ETH为0，即不需要交易，所以：

$$
\begin{align}
Penalty\ Term
&=\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}(1-\frac{1}{\sqrt{H}})+L(\frac{1}{\sqrt{L}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_L] \\
&=k\lambda((1-\frac{1}{\sqrt{H}})+L(\frac{1}{\sqrt{L}}-\frac{1}{\sqrt{H}})\frac{sinh(b\sqrt{2r})}{sinh((b-a)\sqrt{2r})})
\end{align}
$$

其中：
$$
a=\frac{ln(L)}{\sigma},b=\frac{ln(H)}{\sigma}
$$

### 2.当运动为0drift布朗运动，且为美式定价的时候，由于美式定价的平仓时机只有两种价格状态$[L_1,L_2]$，所以：

$$
\begin{align}
Penalty\ Term
&=\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}(1-\frac{1}{\sqrt{H}})+L_1(\frac{1}{\sqrt{L_1}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_{L_1}]+L_2(\frac{1}{\sqrt{L_2}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_{L_2}] \\
&=k\lambda((1-\frac{1}{\sqrt{H}})+L_1(\frac{1}{\sqrt{L_1}}-\frac{1}{\sqrt{H}})\frac{sinh(b\sqrt{2r})}{sinh((b-a)\sqrt{2r})}+L_2(\frac{1}{\sqrt{L_2}}-\frac{1}{\sqrt{H}})\frac{sinh(-a\sqrt{2r})}{sinh((b-a)\sqrt{2r})})
\end{align}
$$

其中：
$$
a=\frac{ln(L_1)}{\sigma},b=\frac{ln(L_2)}{\sigma}
$$

### 3.当运动为GBM，且为欧式定价的时候，由于欧式定价的平仓时机只有两种价格状态$[L,H]$，其中H状态时持有ETH为0，即不需要交易，所以：

$$
\begin{align}
Penalty\ Term
&=\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}(1-\frac{1}{\sqrt{H}})+L(\frac{1}{\sqrt{L}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_L] \\
&=k\lambda((1-\frac{1}{\sqrt{H}})+L(\frac{1}{\sqrt{L}}-\frac{1}{\sqrt{H}})\frac{sinh(b\sqrt{2r+\mu^2})}{sinh((b-a)\sqrt{2r+\mu^2})})
\end{align}
$$

其中：
$$
a=\frac{ln(L)}{\sigma},b=\frac{ln(H)}{\sigma}
$$

### 4.当运动为GBM，且为美式定价的时候，由于美式定价的平仓时机只有两种价格状态$[L_1,L_2]$，所以：

$$
\begin{align}
Penalty\ Term
&=\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}(1-\frac{1}{\sqrt{H}})+L_1(\frac{1}{\sqrt{L_1}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_{L_1}]+L_2(\frac{1}{\sqrt{L_2}}-\frac{1}{\sqrt{H}})\frac{k}{2-\sqrt{L}-\frac{1}{\sqrt{H}}}E[e^{-r\tau},S_T=S_{L_2}] \\
&=k\lambda((1-\frac{1}{\sqrt{H}})+L_1(\frac{1}{\sqrt{L_1}}-\frac{1}{\sqrt{H}})\frac{sinh(b\sqrt{2r+\mu^2})}{sinh((b-a)\sqrt{2r+\mu^2})}+L_2(\frac{1}{\sqrt{L_2}}-\frac{1}{\sqrt{H}})\frac{sinh(-a\sqrt{2r+\mu^2})}{sinh((b-a)\sqrt{2r+\mu^2})})
\end{align}
$$

其中：
$$
a=\frac{ln(L_1)}{\sigma},b=\frac{ln(L_2)}{\sigma}
$$
