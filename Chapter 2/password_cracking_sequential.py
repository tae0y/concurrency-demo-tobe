#!/usr/bin/env python3.9

"""Program for cracking the password consisting with only numbers using brute
force approach sequentially"""

import time
import math
import hashlib
import typing as T
import multiprocessing


ChunkRange = T.Tuple[int,int]


def get_chunks(num_ranges: int, length: int) -> T.Iterator[ChunkRange]:
    max_number = int(math.pow(10,length)-1)
    chunk_starts = [int(max_number/num_ranges*i) for i in range(num_ranges)]
    chunk_ends = [start_point-1 for start_point in chunk_starts[1:]] + [max_number]
    return zip(chunk_starts, chunk_ends)


def get_combinations(*, length: int, min_number: int = 0,
                     max_number: T.Optional[int] = None) -> T.List[str]:
    """Generate all possible password combinations"""
    combinations = []
    if not max_number:
        # calculating maximum number based on the length
        max_number = int(math.pow(10, length) - 1)

    # go through all possible combinations in a given range
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        # fill in the missing numbers with zeros
        zeros = "0" * (length - len(str_num))
        combinations.append("".join((zeros, str_num)))
    return combinations


def get_crypto_hash(password: str) -> str:
    """"Calculating cryptographic hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str,
                   possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    # compare the resulted cryptographic hash with the one stored in the system
    return expected_crypto_hash == actual_crypto_hash


def crack_chunk(crypto_hash: str, length: int, chunk_start: int, chunk_end: int):
    combinations = get_combinations(length=length, min_number=chunk_start, max_number=chunk_end)
    for combination in combinations:
        if check_password(crypto_hash, combination):
            print(f"PASSWORD CRACKED: {combination}")
            break #TODO: 처리 완료되면 다른 프로세스들도 중지하기


def crack_password(crypto_hash: str, length: int) -> None:
    """Brute force the password combinations"""
    start_time = time.perf_counter()
    num_cores = multiprocessing.cpu_count()
    print(f"Processing number combinations in parallel with {num_cores} core")
    chunks = get_chunks(num_cores, length)

    with multiprocessing.Pool(processes=num_cores) as pool: #멀티 프로세스
        results = pool.starmap(
            crack_chunk,
            [(crypto_hash, length, chunk_start, chunk_end) for chunk_start, chunk_end in chunks]
        )
    for result in results: #결과 확인
        if result is not None:
            print("PASSWORD FOUND: {result}")
            break

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")


if __name__ == "__main__":
    crypto_hash = \
        "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password(crypto_hash, length)

"""
> sequenital



> parallel
Processing number combinations in parallel with 8 core
PASSWORD CRACKED: 87654321
PROCESS TIME: 12.591025916000035
"""