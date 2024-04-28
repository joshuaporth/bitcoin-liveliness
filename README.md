# bitcoin-liveliness
Measuring the Liveliness of Bitcoin 🚀

## Liveliness
> Liveliness is a metric which provides insights into shifts in macro HODLing behavior, helping to identify trends in long term holder accumulation or spending.

__Liveliness__ was coined by [Tamas Blummer in 2018](https://medium.com/@tamas.blummer/liveliness-of-bitcoin-174001d016da).

Tamas originally used the concept of "stake" to define __Liveliness__. We now recognize that _Coin Days Destroyed (CDD)_, coined by [ByteCoin in 2011](https://bitcointalk.org/index.php?topic=6172.msg90789#msg90789), is equivalent to Tamas' concept of "stake".

The _Cumulative CDD_ is equivalent to "sum of stakes used" (the numerator in Tamas' algorithm).

Furthermore, every Bitcoin in circulation accumulates one coin day per day. The sum of all accumulated coin days is the "sum of all stakes existed" (the denominator in Tamas' algorithm).

Below are a couple articles that shed more light on Liveliness:
- https://academy.glassnode.com/indicators/liveliness/liveliness
- https://bitcoinmagazine.com/markets/how-liveliness-can-track-bitcoin-price-bull-and-bear-cycles


## TODO
- [ ] Convert LevelDB data to csv or sqlite
- [ ] Create Liveliness chart using [Dash][dash]

[dash]: https://dash.plotly.com/introduction