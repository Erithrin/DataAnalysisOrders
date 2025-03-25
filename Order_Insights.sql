#--find top 10 highest revenue generating products 
select 
	product_id
from
	df_orders
order by 
	profit desc
limit 10;
	


#top 5 highest selling products in each region
select * from
(select 
	region,
	product_id,   
    sum(sales_price) as total_sales,
    row_number() over (partition by region order by sum(sales_price) desc)as rn
from 	
	df_orders
group by 
	1,2) A
where rn <=5 ;


#month over month growth comparison for 2022 and 2023 sales eg : jan 2022 vs jan 2023
select * from df_orders;
select
	date_format(order_date, '%m') as month,
    sum(case when date_format(order_date, '%Y') = 2022 then sales_price else 0 end) as sales_2022,
    sum(case when date_format(order_date, '%Y') = 2023 then sales_price else 0 end) as sales_2023   
from 
	df_orders
group by 
	1
order by 
	month;


#for each category which month had highest sales 
select * from df_orders;
select * from (select
	category,
    date_format(order_date,'%M-%Y') as sales_date,
    sum(sales_price),
    row_number() over (partition by category order by sum(sales_price) desc) as row_num
from 
	df_orders
group by 
	category,date_format(order_date,'%M-%Y')) A
where row_num = 1;


#which sub category had highest growth by profit in 2023 compare to 2022
select distinct(sub_category), category from df_orders;
with cte as (select 
	sub_category,
    sum(case when year(order_date) = 2022 then sales_price else 0 end) as sales_2022,
    sum(case when year(order_date) = 2023 then sales_price else 0 end) as sales_2023
from
	df_orders
group by sub_category
)
select
	sub_category,
    sales_2022,
    sales_2023,
    sales_2023-sales_2022 as growthYoY,
    concat(round((sales_2023-sales_2022)/sales_2022 * 100,2),'%') as growth_percentage
from 
	cte
group by 
	1
order by (sales_2023-sales_2022)/sales_2022 * 100 desc
limit 1;
    
