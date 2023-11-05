async def get_user_avatars_view(
        user_id: int,
        offset: int,
        limit: int,
        engine: AsyncEngine,
        created_at: datetime
) -> list[Row]:
    async with engine.begin() as connection:
        cursor_avatars = await connection.execute(
            text(f"""
                {statement}
                where a.user_id=:user_id
                and a.is_archived=false and a.deleted_at is null
                and a.created_at <= :created_at
                order by a.created_at desc
                offset :offset rows fetch next :limit rows only
            """), {
                "offset": offset,
                "limit": limit,
                "user_id": user_id,
                "created_at": created_at
            },
        )
    return cursor_avatars.all()