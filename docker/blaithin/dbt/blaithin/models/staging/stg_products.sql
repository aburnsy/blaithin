with products as (

    select
        source,
        category,
        product_name,
        img_url,
        description,
        price,
        size,
        stock,
        quantity,
        input_date,
        source_url,
        product_url,
        row_number() over (partition by source, input_date, product_name, size, cast(price as string), stock order by product_url asc) as product_number
    from {{ source('blaithin', 'products') }}

)

select * from products
where product_number = 1

