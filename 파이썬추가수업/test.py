def avg_max_min(student, *args):
    avg =  sum(args) / len(args)
    max_score = max(args)
    min_score = min(args)
    
    if avg >= 90:
        grade = 'A'
    elif avg >= 80:
        grade = 'B'
    elif avg >= 70:
        grade = 'C'
    elif avg >= 60:
        grade = 'D'
    else:
        grade = 'F'
    return grade, avg, max_score, min_score

while True:
    student = input("학생의 이름을 입력하세요 (종료하려면 '종료' 입력): ")
    if student == '종료':
        break
    scores = input("점수를 입력하세요 (공백으로 구분): ")
    scores = list(map(int, scores.split()))
    if not scores:
        print("점수를 입력하지 않았습니다. 다시 시도하세요.")
        continue
    grade, avg, max_score, min_score = avg_max_min(student, *scores)
    print(f"{student}의 평균: {avg:.2f}, 최고 점수: {max_score}, 최저 점수: {min_score}, 학점: {grade}")
    print("프로그램을 종료합니다.")

