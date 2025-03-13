print('Hello Mars')

try:
    with open('./mission_computer_main.log', 'r') as log_file:
        log_content = log_file.readlines()

    # 로그를 역순으로 정렬한 것을 보고서 형식으로 작성
    sorted_log_content = sorted(log_content[1:], key=lambda x: x.split(',')[0], reverse=True)

    markdown_content = '# Log Analysis Report\n\n'
    markdown_content += '### Log Entries\n\n'
    markdown_content += '| Timestamp | Event | Message |\n'
    markdown_content += '| --- | --- | --- |\n'

    problematic_markdown_content = '# Problematic Log Entries\n\n'
    problematic_markdown_content += '| Timestamp | Event | Message |\n'
    problematic_markdown_content += '| --- | --- | --- |\n'

    for line in sorted_log_content:
        timestamp, event, message = line.strip().split(',')
        markdown_content += f"| {timestamp} | {event} | {message} |\n"

        # 문제가 되는 키워드를 저장
        if 'unstable' in message or 'explosion' in message:
            problematic_markdown_content += f'| {timestamp} | {event} | {message} |\n'

    # 전체 보고서 저장
    with open('./log_analysis.md', 'w') as markdown_file:
        markdown_file.write(markdown_content)

    # 문제가 되는 부분 따로 저장
    with open('./problematic_log_entries.md', 'w') as problematic_file:
        problematic_file.write(problematic_markdown_content)

    print('로그 내용을 시간의 역순으로 Markdown 형식으로 성공적으로 변환하고 저장했습니다.')
    print(f'문제가 되는 로그 엔트리 파일을 저장했습니다.')

except FileNotFoundError:
    print('오류: 파일을 찾을 수 없습니다.')
except Exception as e:
    print(f'예상치 못한 오류가 발생했습니다: {e}')
