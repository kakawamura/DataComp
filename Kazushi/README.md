## Database

#### Login to Database

```
psql -d  yakiniku
```

#### item

Query for creating item table.
```sql
CREATE TABLE item (
  item_id int8,
  item_detail_id int8,
  color char(016),
  color_category char(016),
  size char(016),
  item_category_1 char(016),
  item_category_2 char(016),
  shop_id int8,
  brand_id int8
);
```

Import item.csv to item table.
```sql
COPY item (item_id,item_detail_id,color,color_category,size,item_category_1,item_category_2,shop_id,brand_id) FROM '/Users/yakiniku/data/item.csv' WITH CSV;
```

#### favorite_shop

Query for creating favorite_shop table.
```sql
CREATE TABLE favorite_shop (
  customer_id int8,
  registration_date char(016),
  shop_id int8
);
```

Import favorite_shop.csv to item table.
```sql
COPY favorite_shop (customer_id, registration_date, shop_id) FROM '/Users/yakiniku/data/favorite_shop.csv' CSV HEADER;
```

#### item_order

Query for creating table.
```sql
CREATE TABLE item_order (
  customer_id int8,
  order_id int8,
  reservation_flag int2,
  device int2,
  order_date char(016),
  additional_fee int8
);
```

Import order.csv to item table.
```sql
COPY item_order (customer_id,order_id,reservation_flag,device,order_date,additional_fee) FROM '/Users/yakiniku/data/order.csv' CSV HEADER;
```

#### item_order_detail

Query for creating table.
```sql
CREATE TABLE item_order_detail (
  order_id int8,
  order_detail_id int2,
  item_id int8,
  item_detail_id int2,
  sale_item_flag int2,
  order_amount int8,
  quantity int2
);
```

Import order_detail.csv to item table.
```sql
COPY item_order_detail (order_id,order_detail_id,item_id,item_detail_id,sale_item_flag,order_amount,quantity) FROM '/Users/yakiniku/data/order_detail.csv' CSV HEADER;
```

#### member

Query for creating table.
```sql
CREATE TABLE member (
  enquete_flag int2,
  customer_id int8,
  sex int2,
  age char(008),
  registration_date char(016),
  withdrawal_date char(016),
  prefectures char(016)
);
```

Import member.csv to item table.
```sql
COPY member(enquete_flag,customer_id,sex,age,registration_date,withdrawal_date,prefectures) FROM '/Users/yakiniku/data/membe.csv' CSV HEADER;



### enquete

```sql
CREATE TABLE enquete (
  answer_date char(016),
  customer_id int8,
  Q1_1 int2,Q1_2 int2,Q1_3 int2,Q1_4 int2,Q1_5 int2,Q1_6 int2,Q1_7 int2,Q1_8 int2,Q1_9 int2,Q1_10 int2,Q1_11 int2,Q1_12 int2,

  Q2_1,Q2_2,Q2_3,Q2_4,Q2_5,Q2_6,Q2_7,Q2_8,Q2_9,Q2_10,Q2_11,Q2_12,Q2_13,Q2_14,Q3_1,Q3_2,Q3_3,Q3_4,Q3_5,Q3_6,Q3_7,Q3_8,Q3_9,Q3_10,Q3_11,Q3_12,Q3_13,Q3_14,Q3_15,Q3_16,Q3_17,Q3_18,
  Q3_19,
  Q4,
  Q5,
  Q6_1,Q6_2,Q6_3,Q6_4,Q6_5,Q6_6,Q6_7,Q6_8,Q6_9,
  Q6_10,
  Q7_1,Q7_2,Q7_3,Q7_4,Q7_5,Q7_6,Q7_7,Q7_8,Q7_9,Q7_10,Q7_11,
  Q7_12,
  Q8_1,Q8_2,Q8_3,Q8_4,Q8_5,Q8_6,Q8_7,Q8_8,Q8_9,Q8_10,Q8_11,Q8_12,Q8_13,Q8_14,Q8_15,Q8_16,Q8_17,Q8_18,Q8_19,Q8_20,Q8_21,Q8_22,Q8_23,Q8_24,Q8_25,Q8_26,Q8_27,Q8_28,Q8_29,Q8_30,Q8_31,
  Q8_32,
  Q9_1,Q9_2,Q9_3,Q9_4,Q9_5,Q9_6
)


```
```
