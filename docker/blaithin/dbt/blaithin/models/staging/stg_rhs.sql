with rhs as (

    select
        id,
        -- source,
        plant_url,
        botanical_name,
        common_name,
        plant_type,
        description,
        is_rhs_award_winner,
        is_pollinator_plant,
        height,
        spread,
        time_to_ultimate_spread,
        soils,
        moisture,
        ph,
        sun_exposure,
        aspect,
        exposure,
        hardiness,
        foliage,
        habit

    from {{ source('blaithin', 'rhs') }}

)

select * from rhs

