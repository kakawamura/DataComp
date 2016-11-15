select
	*
into 
	log_comp_75
from
	log_comp
where
	customer_id not in
		(
			select
				customer_id
			from
				log_comp
			group by
				customer_id
			order by
				count(*)
			desc
			limit 25375
		);
	

alter table log_comp_75 add id serial; 
