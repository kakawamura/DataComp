## Database

#### Login to Database

```
psql -d  yakiniku
```

#### ITEM Table

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



