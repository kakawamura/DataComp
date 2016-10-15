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
```
