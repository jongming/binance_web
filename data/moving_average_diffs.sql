
select ticker, close, volume, sma200, vol50, d21, d50, d200 FROM 
(
select 
--*,
ticker, close, volume, vol50, sma200, 
ROUND(abs(ema21-ema8)/ema21,4) *100 as  'd21'
,ROUND(abs(sma50-ema21)/sma50,4) *100 as 'd50'
,ROUND(abs(sma200-sma50)/sma200,4) *100 as 'd200'
from historical_data 
where 
--ticker = 'AAPL' 
on_date = '2022-06-10'
ORDER by 
ticker 
--on_date DESC
)
WHERE 
--close > sma50 AND
d21 < 0.1 AND
d50 < 0.1 AND
d50 not NULL