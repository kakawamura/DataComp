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
