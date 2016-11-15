
CREATE TABLE item_has_no_brand AS(
SELECT *
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
