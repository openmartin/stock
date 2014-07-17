DROP TABLE stock_analysis_stockprofit;
DROP TABLE stock_analysis_stockholder;
DROP TABLE stock_analysis_stocktraderecord;


SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit >0
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit >0 AND(corp_code LIKE '51%' OR corp_code LIKE '15%')
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit >0 AND(corp_code LIKE '11%' OR corp_code LIKE '12%')
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit >0 AND(corp_code LIKE '00%' OR corp_code LIKE '60%')


SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit <0
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit <0 AND(corp_code LIKE '51%' OR corp_code LIKE '15%')
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit <0 AND(corp_code LIKE '11%' OR corp_code LIKE '12%')
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit <0 AND(corp_code LIKE '00%' OR corp_code LIKE '60%')
SELECT SUM(profit) FROM stock_analysis_stockprofit WHERE profit <0 AND remarks='股息红利税补'



