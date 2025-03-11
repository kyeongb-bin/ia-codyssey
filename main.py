try:
    with open('mission_computer_main.log', 'r') as log_file:
        log_content = log_file.readlines()

    markdown_content = "# Log Analysis Report\n\n"
    markdown_content += "### Log Entries\n\n"
    markdown_content += "| Timestamp | Event | Message |\n"
    markdown_content += "| --- | --- | --- |\n"

    for line in log_content[1:]:
        timestamp, event, message = line.strip().split(',')
        markdown_content += f"| {timestamp} | {event} | {message} |\n"

    with open('log_analysis.md', 'w') as markdown_file:
        markdown_file.write(markdown_content)

    print('로그 내용을 Markdown 형식으로 성공적으로 변환하고 저장했습니다.')

except FileNotFoundError:
    print('오류: 파일을 찾을 수 없습니다.')
except Exception as e:
    print(f'예상치 못한 오류가 발생했습니다: {e}')
