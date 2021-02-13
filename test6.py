import time
import asyncio

async def find_users_async(n,a):
    for i in range(1, n + 1):
        a[n-1]+=i
        await asyncio.sleep(1)
    print(f'> 총 {n} 명 사용자 비동기 조회 완료!')

async def process_async(a):
    start = time.time()
    await asyncio.wait([
        find_users_async(3,a),
        find_users_async(2,a),
        find_users_async(1,a),
    ])
    end = time.time()
    print(f'>>> 비동기 처리 총 소요 시간: {end - start}')

a=[0 for i in range(3)]
if __name__ == '__main__':
    asyncio.run(process_async(a))
    print(a)