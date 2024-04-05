with products as (

    select
        source,
        source_url,
        product_url,
        category,
        product_name,
        img_url,
        description,
        price,
        size,
        stock,
        quantity,
        input_date

    from {{ source('blaithin', 'products') }}

)

select * from products

