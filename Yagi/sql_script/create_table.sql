
CREATE TABLE item_has_no_brand AS(
SELECT row_number() over()-1  new_item_id,
       *
  FROM (SELECT DISTINCT item_id,
               item_detail_id,
               color,
               color_category,
               size,
               item_category_1,
               item_category_2,
               shop_id
          FROM item) AS tmp
);


CREATE TABLE log_comp AS (
SELECT iod.order_id,
       iod.order_detail_id,
       io.customer_id,
       m.sex,
       m.age,
       m.registration_date,
       m.withdrawal_date,
       m.prefectures,
       io.reservation_flag,
       io.device,
       io.order_date,
       io.additional_fee,
       i.new_item_id,
       iod.item_id,
       iod.item_detail_id,
       i.color,
       i.color_category,
       i.size,
       i.item_category_1,
       i.item_category_2,
       i.shop_id,
       iod.sale_item_flag,
       iod.order_amount,
       iod.quantity
  FROM item_order_detail iod
       LEFT JOIN item_order io
       ON iod.order_id = io.order_id
       LEFT JOIN member m
       ON io.customer_id = m.customer_id
       LEFT JOIN item_has_no_brand i
       ON iod.item_id = i.item_id AND iod.item_detail_id = i.item_detail_id 
);



-- take 5429.3 seconds
CREATE TABLE item_analyzed AS (
SELECT *
  FROM item_has_no_brand
 WHERE new_item_id IN (SELECT new_item_id
                   	     FROM (SELECT new_item_id,
                   	                MIN(item_category_1) AS item_category_1,
                   	                COUNT(*)
                   	           FROM log_comp
                   	          GROUP BY new_item_id
                   	         HAVING COUNT(*) >=5) as foo
                   	   WHERE NOT EXISTS (SELECT *
                   	                       FROM item_has_no_brand
                   	                      WHERE foo.item_category_1 IN ('その他', 'インテリア', 'コスメ/香水', 'マタニティ・ベビー', '水着/着物・浴衣', '財布/小物', '雑貨/ホビー/スポーツ', '音楽/本・雑誌', '食器/キッチン')))
);


CREATE TABLE log_comp_tmp AS (
SELECT *
  FROM log_comp
 WHERE new_item_id IN (SELECT new_item_id
                     FROM item_analyzed)
);


CREATE TABLE log_comp_tmp2 AS (
SELECT *
  FROM log_comp_tmp
 WHERE customer_id IN (SELECT customer_id
                         FROM log_comp_tmp
                        GROUP BY customer_id
                       HAVING COUNT(*)>=5 AND COUNT(*)<120)
);



CREATE TABLE member_analyzed AS (
SELECT *,
       row_number() over()-1  new_customer_id
  FROM member
 WHERE customer_id IN (SELECT DISTINCT(customer_id)
                         FROM log_comp_tmp2)
);


CREATE TABLE log_comp_analyzed AS (
SELECT l.order_id,
       l.order_detail_id,
       l.customer_id,
       m.new_customer_id,
       l.sex,
       l.age,
       l.registration_date,
       l.withdrawal_date,
       l.prefectures,
       l.reservation_flag,
       l.device,
       l.order_date,
       l.additional_fee,
       l.new_item_id,
       l.item_id,
       l.item_detail_id,
       l.color,
       l.color_category,
       l.size,
       l.item_category_1,
       l.item_category_2,
       l.shop_id,
       l.sale_item_flag,
       l.order_amount,
       l.quantity
  FROM log_comp_tmp2 l
       LEFT JOIN member_analyzed m 
       ON l.customer_id = m.customer_id 
);

DROP TABLE log_comp_tmp, log_comp_tmp2

CREATE TABLE item_analyzed_2 AS (
SELECT *
  FROM item_analyzed
 WHERE new_item_id IN (SELECT DISTINCT(new_item_id)
                         FROM log_comp_analyzed)
);

