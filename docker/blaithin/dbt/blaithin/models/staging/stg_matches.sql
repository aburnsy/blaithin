with matches as (

    select
        product_name,
        -- name as matched_name,
        id

    from {{ source('blaithin', 'matches') }}

)

select * from matches

