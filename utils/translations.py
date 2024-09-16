
conditions_for_user = {
    True: 'Да',
    False: 'Нет'
}


async def transform_for_cond(arr):
    for _ in range(len(arr)):
        arr[_].auth = conditions_for_user[arr[_].auth]
        arr[_].superuser = conditions_for_user[arr[_].superuser]

    return arr