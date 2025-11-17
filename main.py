import requests, hashlib, json

API_URL = "https://api.close.com/buildwithus"

def get_key_and_traits() -> tuple[str, list[str]]:
    """
    Enclosed are some traits that [Joe](https://www.linkedin.com/in/jkemp101/) believes
    great engineers exhibit.

    :return: Returns the key and traits retrieved from the GET endpoint.
    :rtype: tuple[str, list[str]]
    """

    try:
        response = requests.get(url=API_URL)
        response.raise_for_status()

        json_response = response.json()

        key = json_response['key']
        traits = json_response['traits']
        return key, traits
    except Exception as e:
        print(f"An error has occurred: {e}")

def get_blake2b_hash(trait: str, key: str, digest_size=64, encoding: str = 'utf-8'):
    """
    Using the included UTF-8 `key`, construct a JSON array
    using the lowercase hex digest of the blake2b hash for each trait (digest size=64).

    :param trait: A given trait to be hashed.
    :type trait: str
    :param key: A given key that will be changed every 24 hours.
    :type key: str
    :param digest_size: A given digest size of 64.
    :param encoding: A given encoding to be used when getting the hexdigest for the hash.
    :type encoding: str
    """

    hash = hashlib.blake2b(key=key.encode(encoding), digest_size=digest_size)
    data = trait.encode(encoding)
    hash.update(data)

    return hash.hexdigest()

def get_hexdigests_for_traits(traits: list[str], key: str) -> list[str]:
    """
    Get the hexdigits using the blake2b hash for the given traits and key.

    :param traits: The given traits that every developer should have.
    :type traits: list[str]
    :param key: The given key that will be changed every 24 hours.
    :type key: str
    :return: The blake2b hashed traits.
    :rtype: list[str]
    """

    hexdigests = []

    for trait in traits:
        hexdigest = get_blake2b_hash(trait=trait,key=key)
        hexdigests.append(hexdigest)

    return hexdigests

def post_traits(hexdigests: list[str]):
    """
    POST this bare array back to this endpoint.
    Example array: [\"1f9ec19c7...57fd27e5\", \"79c72b47088...bf13026c\", ...]
    If the hashes are correct you will get a Verification ID you should include in
    your application. 400 responses indicate a problem with the hashes in your array.
    Note, the key rotates each day around midnight EST.

    :param hexdigests: A bare array of hexdigest hashes to be POSTed.
    :type hexdigests: list[str]
    """
    try:
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url=API_URL, headers=headers, json=hexdigests)
        response.raise_for_status()

        return response.text
    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    try:
        key, traits = get_key_and_traits()

        hexdigests = get_hexdigests_for_traits(traits, key=key)

        verification_id = post_traits(hexdigests)
        print(verification_id)
    except Exception as e:
        print(f"An error has occurred: {e}")