# DBT Spark

[dbt-spark](https://github.com/dbt-labs/dbt-spark)

Includes a docker file to quickly spin up a local spark cluster and thrift server
which dbt-core may connect to for local development projects. When working with Databricks, dbt-databricks should be installed instead.

Running pip install dbt-spark will also install dbt-core.
Macbooks with Apple Silicon M1 M2 chips may need Rosetta installed.

[Materialize and Updating Data Lake / Warehouse Tables with Spark Configs](https://docs.getdbt.com/reference/resource-configs/spark-configs)

Strategies such as insert and overwrite or merge require specific supported underlying file formats such as `delta` or `hudi`.
This allows for maintaining up to date incremental models instead of static stale snapshot data lake tables.

There are similarities to incremental persisted derived tables concept available in Looker BI. Example given updating only the latest day's DAU metric.

```sql
    {{
        config(
            materialized='incremental',
            unique_key='date_day'
        )
    }}

    select
        date_trunc('day', event_at) as date_day,
        count(distinct user_id) as daily_active_users

    from raw_app_data.events


    {% if is_incremental() %}

    -- this filter will only be applied on an incremental run
    where date_day >= (select max(date_day) from {{ this }})

    {% endif %}

    group by 1
```