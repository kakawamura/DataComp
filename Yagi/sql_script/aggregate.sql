-- output = 0
SELECT COUNT(*)
  FROM member m
  WHERE NOT EXISTS (SELECT m.customer_id = l.customer_id FROM log_comp l)

-- output = 0
SELECT COUNT(*)
  FROM item i
  WHERE NOT EXISTS (SELECT i.item_category_2 = l.item_category_2 FROM log_comp l) 

-- output = itemcount_per_customer.csv
SELECT customer_id,
       COUNT(*)
  FROM log_comp
 GROUP BY customer_id;

-- output = quantitycount_per_customer.csv
SELECT customer_id,
       SUM(quantity)
  FROM log_comp
 GROUP BY customer_id;

/*
output =
1   342222 (pc)
2   662230 (smart phone)
3   5228 (galapagos phone)
*/
SELECT device,
       COUNT(*)
  FROM log_comp
 GROUP BY device;

-- output = 695
SELECT COUNT(*)
  FROM log_comp
 WHERE order_amount<0;


-- 103,144
SELECT COUNT(DISTINCT(customer_id))
  FROM member;
 
-- 48,317
SELECT COUNT(*)
  FROM (
SELECT customer_id,
       COUNT(*)
  FROM log_comp
 GROUP BY customer_id
 HAVING COUNT(*) >=5 AND COUNT(*) < 365) as foo


-- 442,563
SELECT COUNT(DISTINCT(item_id))
  FROM item;

-- 7,241
SELECT COUNT(*)
  FROM(SELECT item_id,
              MIN(item_category_1) AS item_category_1,
              COUNT(*)
         FROM log_comp_75
        GROUP BY item_id
       HAVING COUNT(*) >=5) as foo
 WHERE NOT EXISTS (SELECT *
                     FROM item
                    WHERE foo.item_category_1 IN ('その他', 'インテリア', 'コスメ/香水', 'マタニティ・ベビー', '水着/着物・浴衣', '財布/小物', '雑貨/ホビー/スポーツ', '音楽/本・雑誌', '食器/キッチン'))
;

