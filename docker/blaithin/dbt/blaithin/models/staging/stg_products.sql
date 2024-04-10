with raw_products as (

    select
        source,
        category,
        product_name,
        img_url,
        description,
        price,
        size as size_original,
        stock,
        quantity,
        input_date,
        source_url,
        product_url,
        row_number() over (partition by source, input_date, product_name, size, cast(price as string), stock order by product_url asc) as product_number
    from {{ source('blaithin', 'products') }}

),
products as (
    select
        source,
        category,
        product_name,
        img_url,
        description,
        price,
          coalesce(
            IF(size_original LIKE '%bare%', 'Bare Root', NULL),
            upper(replace(regexp_extract(size_original, r'\d?\.?\d+ *[Ll]'), ' ','')),
            lower(replace(regexp_extract(size_original, r'\d+ ?[Cc][Mm]'),' ','')),
            lower(replace(regexp_extract(size_original, r'\d+ ?[Mm]'),' ','')),
            IF(size_original LIKE '%Tree%', 'Unknown', NULL),
            IF(size_original LIKE '%Rootball%', 'Rootball', NULL),
            IF(size_original LIKE '%Bowl%', 'Bowl', NULL),
            IF(size_original LIKE '%Seed%', 'Seeds', NULL),
            lower(replace(regexp_extract(size_original, r'\d+ ?[Cc]rowns?'),' ','')),
            IF(size_original LIKE '%Plant%', 'Unknown', NULL),
            IF(lower(size_original) LIKE '%pack%', 'Unknown', NULL),
            IF(size_original LIKE '%Airpot%', 'Airpot', NULL),
            IF(size_original LIKE '%Potted%', 'Potted', NULL),
            IF(lower(size_original) LIKE '%cont%', 'Unknown', NULL),
            CASE regexp_extract(size_original, r'P ?\d+\.?\d')
                WHEN 'P8.5' THEN '8cm'
                WHEN 'P9' THEN '9cm'
                WHEN 'P9.5' THEN '9cm'
                WHEN 'P10' THEN '1L'
                WHEN 'P10.5' THEN '1L'
                WHEN 'P11' THEN '1L'
                WHEN 'P12' THEN '2L'
                WHEN 'P13' THEN '2L'
                WHEN 'P14' THEN '3L'
                WHEN 'P15' THEN '3L'
                WHEN 'P16' THEN '4L'
                WHEN 'P17' THEN '4L'
                WHEN 'P18' THEN '5L'
                WHEN 'P19' THEN '6L'
                WHEN 'P20' THEN '7L'
                WHEN 'P25' THEN '10L'
                WHEN 'P30' THEN '15L'
                ELSE NULL
            END,
            'Unknown',
        ) as size,
        size_original,
        stock,
        quantity,
        input_date,
        source_url,
        product_url,
    from raw_products
    where product_number = 1
)

select * from products