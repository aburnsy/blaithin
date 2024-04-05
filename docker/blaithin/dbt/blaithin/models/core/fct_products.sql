with stg_products as  (
    select * from {{ ref('stg_products' )}}
),

max_date as (
    select
        max(input_date) as input_date
    from stg_products
),

latest_products as (
    select * from stg_products
    join max_date using (input_date)
),

matches as  (
    select * from {{ ref('stg_matches' )}}
),

rhs as  (
    select * from {{ ref('stg_rhs' )}}
),

products_fact as (
    select 
        source,
        source_url,
        product_url,
        -- category,
        product_name,
        img_url,
        p.description as source_description,
        price,
        size,
        stock,
        quantity,
        case when quantity > 0 then True else False end as is_bulk_deal,
        -- input_date
        plant_url,
        botanical_name,
        common_name,
        plant_type,
        rhs.description as rhs_description,
        is_rhs_award_winner,
        is_pollinator_plant,
        height,
        spread,
        time_to_ultimate_spread as time_to_ultimate_height,
        soils,
        moisture,
        ph,
        sun_exposure,
        aspect,
        exposure,
        hardiness,
        foliage,
        habit    
    from latest_products p
    inner join matches m on p.product_name = m.product_name
    inner join rhs on m.id = rhs.id
)

select * from products_fact