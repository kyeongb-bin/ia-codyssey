def caesar_cipher_decode(target_text):
    '''
    카이사르 암호를 자리수(shift)별로 해독하여 결과를 출력합니다.
    영어 알파벳(대소문자)만 변환하며, 나머지는 그대로 둡니다.
    '''
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num_letters = 26

    for shift in range(1, num_letters + 1):
        decoded = ''
        for char in target_text:
            if char in alphabet_lower:
                idx = (alphabet_lower.index(char) - shift) % num_letters
                decoded += alphabet_lower[idx]
            elif char in alphabet_upper:
                idx = (alphabet_upper.index(char) - shift) % num_letters
                decoded += alphabet_upper[idx]
            else:
                decoded += char
        print('[' + str(shift) + '] ' + decoded)
    print('\n자리수를 눈으로 확인한 후, 해독된 번호를 입력하세요.')


def load_dictionary():
    '''
    간단한 영어 단어 사전(보너스용).
    '''
    return {
        'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but', 'his',
        'from', 'they', 'say', 'her', 'she', 'will', 'one', 'all', 'would', 'there', 'their', 'what',
        'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can',
        'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good',
        'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its',
        'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
        'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
    }


def caesar_cipher_decode_with_dict(target_text):
    '''
    보너스: 사전 매칭 시 자동 중단
    '''
    dictionary = load_dictionary()
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num_letters = 26

    for shift in range(1, num_letters + 1):
        decoded = ''
        for char in target_text:
            if char in alphabet_lower:
                idx = (alphabet_lower.index(char) - shift) % num_letters
                decoded += alphabet_lower[idx]
            elif char in alphabet_upper:
                idx = (alphabet_upper.index(char) - shift) % num_letters
                decoded += alphabet_upper[idx]
            else:
                decoded += char
        print('[' + str(shift) + '] ' + decoded)
        words = decoded.lower().split()
        for word in words:
            if word in dictionary:
                print(str(shift) + '번째 자리수에서 "' + word + '" 단어 발견! 결과를 저장합니다.')
                return shift, decoded
    return None, None


def main():
    try:
        with open('password.txt', 'r') as f:
            target_text = f.read().strip()
    except FileNotFoundError:
        print('password.txt 파일이 존재하지 않습니다.')
        return
    except Exception as e:
        print('파일을 읽는 중 오류가 발생했습니다:', e)
        return

    shift, result = caesar_cipher_decode_with_dict(target_text)
    if result:
        try:
            with open('result.txt', 'w') as f:
                f.write(result)
            print('result.txt에 결과가 저장되었습니다.')
        except Exception as e:
            print('파일 저장 중 오류가 발생했습니다:', e)
        return

    caesar_cipher_decode(target_text)

    try:
        selected = int(input('해독된 번호를 입력하세요: '))
        if not (1 <= selected <= 26):
            print('1~26 사이의 숫자를 입력하세요.')
            return
    except ValueError:
        print('숫자를 입력하세요.')
        return

    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num_letters = 26
    decoded = ''
    for char in target_text:
        if char in alphabet_lower:
            idx = (alphabet_lower.index(char) - selected) % num_letters
            decoded += alphabet_lower[idx]
        elif char in alphabet_upper:
            idx = (alphabet_upper.index(char) - selected) % num_letters
            decoded += alphabet_upper[idx]
        else:
            decoded += char

    try:
        with open('result.txt', 'w') as f:
            f.write(decoded)
        print('result.txt에 결과가 저장되었습니다.')
    except Exception as e:
        print('파일 저장 중 오류가 발생했습니다:', e)


if __name__ == '__main__':
    main()
