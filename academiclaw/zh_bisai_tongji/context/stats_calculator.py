# # # By: ThrasH

# # # Last Update Date: 13/8/2025

import os
import csv
import statistics
from collections import defaultdict
from datetime import datetime

# # #输入格式：
# 输入是一个.csv表格，其记录了一场比赛的相关数据。
# 第一行第一列如果是数字6657，则开始读入后面的内容。
# 第二行填入3个数，依次代表比赛进行的年，月，日。
# 第三行填入一个数n，表示队伍的总数，一个数x，手动设置，调控用
# 接着n行每行填入了五列，第一列代表队伍名；第二列一个数字代表队伍在打这次比赛前的已有排名，如果没有的话则为“*”；第三列一个数字代表队伍在这次比赛的排名。第四列有-1代表弃赛，第五列为手动设置的调分参数
# 接下来若干行代表每一场的记录。
# 对其中的任意一行，第一列一个数字代表该场比赛的性质：如果是1则为BO1，3则为BO3，5则为BO5。
# 第二列一个数字代表该场比赛的重要程度，第三列和第四列代表该场比赛的两个参赛队伍。
# 从第五列起，对每三列有以下的规律：其中的第一列代表第一个队伍的单局比分，第二列代表第二个队伍的单局比分，第三列代表该局所用地图，如果没有则为“*”。
# 对第一局比赛，（如果有的话）-1是迟到，-2是弃赛，-3是判负，另一个填0.
# 读到某一行的第一列为数字123321时，终止读入。

#读取.csv文件
def parse_csv(file_path):
    with open(file_path, newline='', encoding='gbk') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    if data[0][0] != '6657':
        raise ValueError("Invalid file format: First cell should be 6657")

    # Parse date
    year, month, day = map(int, data[1][:3])

    # Parse number of teams
    n = int(data[2][0])  # 队伍总数

    #从第三行第二列读取 x 值
    x = float(data[2][1]) if data[2][1] != '' else 1.0

    # Parse teams
    teams = {}
    for i in range(n):
        team_name = data[3 + i][0]
        prev_rank = data[3 + i][1] if data[3 + i][1] != '*' else None
        current_rank = int(data[3 + i][2])
        forfeit_flag = int(data[3 + i][3]) if data[3 + i][3] != '' else 0  # 第4列：弃赛标志
        fourth_integral_weight = float(data[3 + i][4]) if data[3 + i][4] != '' else 1.0  # 第5列：第四个积分的权重
        teams[team_name] = {
            'prev_rank': prev_rank,
            'current_rank': current_rank,
            'bo1_wins': 0,
            'bo1_losses': 0,
            'bo1_count': 0,  # BO1比赛数量
            'bo3_wins': 0,
            'bo3_losses': 0,
            'bo3_count': 0,  # BO3比赛数量
            'bo5_wins': 0,
            'bo5_losses': 0,
            'bo5_count': 0,  # BO5比赛数量
            'match_wins': 0,  # 获胜场数
            'match_losses': 0,  # 失败场数
            'match_count': 0,  # 比赛场数
            'game_wins': 0,  # 胜利局数
            'game_losses': 0,  # 失败局数
            'game_count': 0,  # 比赛局数
            'map_stats': defaultdict(lambda: {'wins': 0, 'losses': 0}),  # 每张地图的胜负统计
            'win_streaks': [],  # 记录每场比赛的胜负（1为胜，0为负）
            'win_streaks_count': [],  # 记录连胜次数（>=3的连胜）
            'late_count': 0,
            'forfeit_count': 0,
            'forfeit_flag': forfeit_flag, #整届弃赛标志
            'successful_matches': [],  # 记录成功参与的比赛（没有迟到、弃赛或判负）
            'fourth_integral_weight': fourth_integral_weight
        }

    # Parse matches
    matches = []
    total_match_type_importance = 0  # 记录所有比赛的 match_type * importance 之和
    total_matches = 0  # 记录比赛总场数

    for row in data[3 + n:]:
        if row[0] == '123321':
            break
        if not row[0]:  # 忽略空行
            continue
        match_type = int(row[0])
        importance = int(row[1])
        team1 = row[2]
        team2 = row[3]
        scores = row[4:]
        match = {
            'type': match_type,
            'importance': importance,
            'team1': team1,
            'team2': team2,
            'scores': []
        }
        for i in range(0, len(scores), 3):
            if i + 2 >= len(scores):  # 确保不越界
                break
            score1 = scores[i] if scores[i] != '' else '0'
            score2 = scores[i + 1] if scores[i + 1] != '' else '0'
            map_name = scores[i + 2] if scores[i + 2] != '*' and scores[i + 2] != '' else None
            match['scores'].append((score1, score2, map_name))
        matches.append(match)

        # 更新总比赛场数和 match_type * importance 之和
        total_matches += 1
        total_match_type_importance += match_type * importance

    # 计算比赛等级参数
    if total_matches > 0:
        competition_level = ((n ** 2 * total_match_type_importance) / total_matches) ** 0.25
    else:
        competition_level = 0  # 如果没有比赛，等级参数为0

    # Process matches
    for match in matches:
        team1 = match['team1']
        team2 = match['team2']
        scores = match['scores']
        match_type = match['type']
        importance = match['importance']

        # Update match count
        teams[team1]['match_count'] += 1
        teams[team2]['match_count'] += 1

        # Check for special scores in the first game
        first_score1, first_score2, _ = scores[0]
        if first_score1 in ['-1', '-2', '-3'] or first_score2 in ['-1', '-2', '-3']:
            if first_score1 in ['-1', '-2', '-3']:
                losing_team = team1
                winning_team = team2
                special_score = first_score1
            else:
                losing_team = team2
                winning_team = team1
                special_score = first_score2

            # Update match result
            teams[winning_team]['match_wins'] += 1
            teams[losing_team]['match_losses'] += 1

            # Update special counts
            if special_score == '-1':
                teams[losing_team]['late_count'] += 1
            elif special_score == '-2':
                teams[losing_team]['forfeit_count'] += 1

            # Skip further processing for this match
            continue

        # 记录成功参与的比赛
        teams[team1]['successful_matches'].append((match_type, importance))
        teams[team2]['successful_matches'].append((match_type, importance))

        # Update BO1/BO3/BO5 counts (only for normal matches)
        if match_type == 1:
            teams[team1]['bo1_count'] += 1
            teams[team2]['bo1_count'] += 1
        elif match_type == 3:
            teams[team1]['bo3_count'] += 1
            teams[team2]['bo3_count'] += 1
        elif match_type == 5:
            teams[team1]['bo5_count'] += 1
            teams[team2]['bo5_count'] += 1

        # Normal match processing
        team1_wins = sum(1 for s in scores if int(s[0]) > int(s[1]))
        team2_wins = sum(1 for s in scores if int(s[1]) > int(s[0]))

        # Update match wins/losses
        if team1_wins > team2_wins:
            teams[team1]['match_wins'] += 1
            teams[team2]['match_losses'] += 1
        else:
            teams[team2]['match_wins'] += 1
            teams[team1]['match_losses'] += 1

        # Update game wins/losses and game count
        for score in scores:
            if int(score[0]) > int(score[1]):
                teams[team1]['game_wins'] += 1
                teams[team2]['game_losses'] += 1
                teams[team1]['game_count'] += 1
                teams[team2]['game_count'] += 1
            elif int(score[1]) > int(score[0]):
                teams[team2]['game_wins'] += 1
                teams[team1]['game_losses'] += 1
                teams[team1]['game_count'] += 1
                teams[team2]['game_count'] += 1

        # Update map wins/losses
        for score in scores:
            map_name = score[2]
            if map_name is None:  # 忽略地图名称为*的情况
                continue
            if int(score[0]) > int(score[1]):
                teams[team1]['map_stats'][map_name]['wins'] += 1
                teams[team2]['map_stats'][map_name]['losses'] += 1
            else:
                teams[team2]['map_stats'][map_name]['wins'] += 1
                teams[team1]['map_stats'][map_name]['losses'] += 1

        # Update BO1/BO3/BO5 wins/losses
        if match_type == 1:
            if team1_wins > team2_wins:
                teams[team1]['bo1_wins'] += 1
                teams[team2]['bo1_losses'] += 1
            else:
                teams[team2]['bo1_wins'] += 1
                teams[team1]['bo1_losses'] += 1
        elif match_type == 3:
            if team1_wins > team2_wins:
                teams[team1]['bo3_wins'] += 1
                teams[team2]['bo3_losses'] += 1
            else:
                teams[team2]['bo3_wins'] += 1
                teams[team1]['bo3_losses'] += 1
        elif match_type == 5:
            if team1_wins > team2_wins:
                teams[team1]['bo5_wins'] += 1
                teams[team2]['bo5_losses'] += 1
            else:
                teams[team2]['bo5_wins'] += 1
                teams[team1]['bo5_losses'] += 1

        # Update win streaks
        if team1_wins > team2_wins:
            teams[team1]['win_streaks'].append(1)
            teams[team2]['win_streaks'].append(0)
        else:
            teams[team2]['win_streaks'].append(1)
            teams[team1]['win_streaks'].append(0)

    # Calculate win streaks
    for team in teams.values():
        streak = 0
        for win in team['win_streaks']:
            if win:
                streak += 1
            else:
                if streak >= 3:
                    team['win_streaks_count'].append(streak)
                streak = 0
        if streak >= 3:
            team['win_streaks_count'].append(streak)

    return {
        'date': (year, month, day),
        'num_teams': n,
        'teams': teams,
        'competition_level': competition_level,  # 比赛等级参数
        'matches': matches,
        'x': x
    }

def get_team_stats(data, team_name):
    team = data['teams'].get(team_name)
    if not team:
        return None

    bo1_win_rate = team['bo1_wins'] / (team['bo1_wins'] + team['bo1_losses']) if (team['bo1_wins'] + team['bo1_losses']) > 0 else 0
    bo3_win_rate = team['bo3_wins'] / (team['bo3_wins'] + team['bo3_losses']) if (team['bo3_wins'] + team['bo3_losses']) > 0 else 0
    bo5_win_rate = team['bo5_wins'] / (team['bo5_wins'] + team['bo5_losses']) if (team['bo5_wins'] + team['bo5_losses']) > 0 else 0
    match_win_rate = team['match_wins'] / (team['match_wins'] + team['match_losses']) if (team['match_wins'] + team['match_losses']) > 0 else 0
    game_win_rate = team['game_wins'] / (team['game_wins'] + team['game_losses']) if (team['game_wins'] + team['game_losses']) > 0 else 0

    # 计算每张地图的胜率
    map_win_rates = {}
    for map_name, stats in team['map_stats'].items():
        total = stats['wins'] + stats['losses']
        if total > 0:
            map_win_rates[f"{map_name}_win_rate"] = stats['wins'] / total
        else:
            map_win_rates[f"{map_name}_win_rate"] = 0

    return {
        'current_rank': team['current_rank'],
        'bo1_count': team['bo1_count'],
        'bo1_win_rate': bo1_win_rate,
        'bo3_count': team['bo3_count'],
        'bo3_win_rate': bo3_win_rate,
        'bo5_count': team['bo5_count'],
        'bo5_win_rate': bo5_win_rate,
        'match_count': team['match_count'],  # 比赛场数
        'match_wins': team['match_wins'],  # 获胜场数
        'game_count': team['game_count'],  # 比赛局数
        'game_wins': team['game_wins'],  # 获胜局数
        'match_win_rate': match_win_rate,
        'game_win_rate': game_win_rate,
        **map_win_rates,  # 将每张地图的胜率合并到输出中
        'win_streaks': team['win_streaks'],
        'win_streaks_count': team['win_streaks_count'],
        'late_count': team['late_count'],
        'forfeit_count': team['forfeit_count'],
    }

def calculate_first_integral(data):
    teams = data['teams']
    n = data['num_teams']
    competition_level = data['competition_level']

    for team_name, team in teams.items():
        current_rank = team['current_rank']
        match_win_rate = team['match_wins'] / (team['match_wins'] + team['match_losses']) if (team['match_wins'] + team['match_losses']) > 0 else 0
        game_win_rate = team['game_wins'] / (team['game_wins'] + team['game_losses']) if (team['game_wins'] + team['game_losses']) > 0 else 0

        # 计算成功参与的比赛 match_type * importance 之和
        sum_match_type_importance = sum(match[0] * match[1] for match in team['successful_matches'])

        # 计算“第一个积分”
        first_integral = (n**2 - current_rank**2) ** (competition_level * data['x']) * (sum_match_type_importance) ** ((match_win_rate + game_win_rate ** 2) / 2)
        team['first_integral'] = first_integral

    return data

def calculate_second_integral(data):
    teams = data['teams']
    first_integrals = [team['first_integral'] for team in teams.values()]
    max_first_integral = max(first_integrals)
    min_first_integral = min(first_integrals)

    # 计算第二个积分
    for team in teams.values():
        if max_first_integral == min_first_integral:
            # 如果所有队伍的“第一个积分”相同，则“第二个积分”均为500
            team['second_integral'] = 500
        else:
            # 线性归一化到 [1, 1000] 区间
            team['second_integral'] = 1 + (team['first_integral'] - min_first_integral) * (999 / (max_first_integral - min_first_integral))

    return data

def calculate_streak_bonus(team):
    """
    计算连胜奖励分
    公式：sum(win_streak_count ** (1 + win_streak_count / 5))
    """
    streak_bonus = 0
    for win_streak_count in team['win_streaks_count']:
        streak_bonus += win_streak_count ** (1 + win_streak_count / 5)
    return streak_bonus

def calculate_upset_bonus(team, matches, teams):
    """
    计算越级挑战分
    公式：sum(1.2 ** (prev_rank的差))，要求双方均有prev_rank且差 >= 8
    """
    upset_bonus = 0
    
    for match in matches:
        first_score1, first_score2, _ = match['scores'][0]
        if first_score1 in ['-1', '-2', '-3'] or first_score2 in ['-1', '-2', '-3']:
            continue
        if match['team1'] == team['name']:
            opponent = match['team2']
            team_wins = sum(1 for s in match['scores'] if int(s[0]) > int(s[1]))
            opponent_wins = sum(1 for s in match['scores'] if int(s[1]) > int(s[0]))
        elif match['team2'] == team['name']:
            opponent = match['team1']
            team_wins = sum(1 for s in match['scores'] if int(s[1]) > int(s[0]))
            opponent_wins = sum(1 for s in match['scores'] if int(s[0]) > int(s[1]))
        else:
            continue

        # 检查双方是否有prev_rank
        if team['prev_rank'] is not None and teams[opponent]['prev_rank'] is not None and team_wins > opponent_wins:
            rank_diff = int(team['prev_rank']) - int(teams[opponent]['prev_rank'])
            if rank_diff >= 8:
                if rank_diff <= 25:
                    upset_bonus += 1.2 ** rank_diff
                else:
                    upset_bonus += 1.2 ** 25

    return upset_bonus

def calculate_high_rank_win_bonus(team, matches, teams):
    """
    计算高位战胜分
    公式：sum(10 ** (1 + 0.1 * (7 - prev_rank)))，要求对手有prev_rank且 <= 6
    """
    high_rank_bonus = 0
    for match in matches:
        first_score1, first_score2, _ = match['scores'][0]
        if first_score1 in ['-1', '-2', '-3'] or first_score2 in ['-1', '-2', '-3']:
            continue
        if match['team1'] == team['name']:
            opponent = match['team2']
            team_wins = sum(1 for s in match['scores'] if int(s[0]) > int(s[1]))
            opponent_wins = sum(1 for s in match['scores'] if int(s[1]) > int(s[0]))
        elif match['team2'] == team['name']:
            opponent = match['team1']
            team_wins = sum(1 for s in match['scores'] if int(s[1]) > int(s[0]))
            opponent_wins = sum(1 for s in match['scores'] if int(s[0]) > int(s[1]))
        else:
            continue

        # 检查对手是否有prev_rank且 <= 6
        if (teams[opponent]['prev_rank'] is not None and int(teams[opponent]['prev_rank']) <= 6 and team_wins > opponent_wins):
            high_rank_bonus += 10 ** (1 + 0.2 * (7 - int(teams[opponent]['prev_rank'])))
    return high_rank_bonus

def calculate_total_bonus(data):
    """
    计算每个队伍的总奖励分
    """
    teams = data['teams']
    matches = data['matches']

    for team_name, team in teams.items():
        team['name'] = team_name  # 为每个队伍添加name字段，方便后续计算
        streak_bonus = calculate_streak_bonus(team)
        upset_bonus = calculate_upset_bonus(team, matches, teams)
        high_rank_bonus = calculate_high_rank_win_bonus(team, matches, teams)

        # 总奖励分
        team['total_bonus'] = streak_bonus + upset_bonus + high_rank_bonus

    return data

def calculate_third_integral(data):
    """
    计算第三个积分
    公式：将 (第二个积分 + 总奖励分) 线性归一化到 [1, 1000] 区间
    """
    teams = data['teams']
    second_integrals = [team['second_integral'] for team in teams.values()]
    total_bonuses = [team['total_bonus'] for team in teams.values()]

    # 计算 (第二个积分 + 总奖励分)
    combined_scores = [second_integral + total_bonus for second_integral, total_bonus in zip(second_integrals, total_bonuses)]
    max_combined = max(combined_scores)
    min_combined = min(combined_scores)

    # 线性归一化到 [1, 1000] 区间
    for team in teams.values():
        if max_combined == min_combined:
            # 如果所有队伍的 combined_scores 相同，则第三个积分统一设置为500
            team['third_integral'] = 500
        else:
            team['third_integral'] = 1 + (team['second_integral'] + team['total_bonus'] - min_combined) * (999 / (max_combined - min_combined))

    return data

def calculate_fourth_integral(data):
    """
    计算第四个积分
    公式：第四个积分 = (第三个积分 * 比赛等级参数 * 平均数) / 中位数
    """
    teams = data['teams']
    third_integrals = [team['third_integral'] for team in teams.values()]

    # 计算中位数和平均数
    median_third_integral = statistics.median(third_integrals)
    mean_third_integral = statistics.mean(third_integrals)

    # 计算第四个积分
    competition_level = data['competition_level']
    for team in teams.values():
        team['fourth_integral'] = team['third_integral'] * team['fourth_integral_weight'] * ((competition_level * data['x']) ** 2 * mean_third_integral / median_third_integral) ** 0.25

    return data

def calculate_fifth_integral(data):
    """
    计算第五个积分
    公式：第五个积分 = 第四个积分 - (迟到次数 * 20 + 弃赛次数 * 25) - (如果迟到次数 >= 3，额外扣100分)
    """
    teams = data['teams']

    for team in teams.values():
        # 计算迟到和弃赛的扣分
        late_penalty = team['late_count'] * 25
        forfeit_penalty = team['forfeit_count'] * 50
        additional_late_penalty = 100 if team['late_count'] >= 3 else 0
        additional_forfeit_penalty = -100 * team['forfeit_flag']

        # 计算总扣分
        total_penalty = late_penalty + forfeit_penalty + additional_late_penalty + additional_forfeit_penalty

        # 计算第五个积分
        team['fifth_integral'] = team['fourth_integral'] - total_penalty

    return data

def print_team_integrals(data):
    """
    输出队伍的积分表格，包含第一个积分、第二个积分、总奖励分、第三个积分、第四个积分和第五个积分
    """
    print("\nTeam Integrals and Bonus:")
    print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        "Team", "First Integral", "Second Integral", "Total Bonus", "Third Integral", "Fourth Integral", "Fifth Integral"
    ))
    for team_name, team in data['teams'].items():
        print("{:<20} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f}".format(
            team_name,
            team['first_integral'],
            team['second_integral'],
            team.get('total_bonus', 0),  # 如果总奖励分不存在，则默认为0
            team.get('third_integral', 0),  # 如果第三个积分不存在，则默认为0
            team.get('fourth_integral', 0),  # 如果第四个积分不存在，则默认为0
            team.get('fifth_integral', 0)  # 如果第五个积分不存在，则默认为0
        ))

def process_single_file(file_path):
    """
    处理单个文件，计算并返回第五个积分
    """
    data = parse_csv(file_path)
    data = calculate_first_integral(data)
    data = calculate_second_integral(data)
    data = calculate_total_bonus(data)
    data = calculate_third_integral(data)
    data = calculate_fourth_integral(data)
    data = calculate_fifth_integral(data)
    return data

def process_multiple_files(directory_path):
    """
    处理多个文件，返回按比赛时间排序的结果
    """
    # 获取目录下所有 .csv 文件
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    # 解析每个文件并记录比赛日期
    file_data = []
    for file_name in csv_files:
        file_path = os.path.join(directory_path, file_name)
        data = parse_csv(file_path)
        file_data.append({
            'file_name': file_name,
            'date': data['date'],
            'data': data
        })
    
    # 按比赛日期由远到近排序
    file_data.sort(key=lambda x: x['date'])
    
    # 计算每个文件的第五个积分
    results = {}
    for file_info in file_data:
        file_name = file_info['file_name']
        data = file_info['data']
        data = calculate_first_integral(data)
        data = calculate_second_integral(data)
        data = calculate_total_bonus(data)
        data = calculate_third_integral(data)
        data = calculate_fourth_integral(data)
        data = calculate_fifth_integral(data)
        
        # 记录每个队伍的第五个积分
        for team_name, team in data['teams'].items():
            if team_name not in results:
                results[team_name] = {}
            results[team_name][file_name] = team['fifth_integral']
    
    return results, file_data

def print_multiple_files_results(results, file_data):
    """
    输出多个文件的第五个积分表格，每个队伍名只出现一次
    """
    # 表头
    header = ["Team"] + [file_info['file_name'] for file_info in file_data]
    print("{:<20}".format(header[0]), end="")
    for col in header[1:]:
        print("{:<15}".format(col), end="")
    print()

    # 表格内容
    for team_name, file_scores in results.items():
        print("{:<20}".format(team_name), end="")
        for file_info in file_data:
            file_name = file_info['file_name']
            score = file_scores.get(file_name, "N/A")
            print("{:<15.4f}".format(score) if score != "N/A" else "{:<15}".format(score), end="")
        print()

def calculate_total_team_score(results, file_data):
    """
    计算总的战队积分
    公式：总的战队积分 = sum(fifth_integral * (1 - 1 / competition_level) ** (Δdate / 50))
    """
    today = datetime.today()
    total_scores = {}

    for team_name, file_scores in results.items():
        total_score = 0
        for file_info in file_data:
            file_name = file_info['file_name']
            if file_name in file_scores:
                # 计算 Δdate（比赛日期和程序运行日期的差值）
                match_date = datetime(*file_info['date'])
                delta_days = (today - match_date).days

                # 获取 competition_level
                competition_level = file_info['data']['competition_level']

                # 计算积分
                fifth_integral = file_scores[file_name]
                total_score += fifth_integral * (1 - 1 / competition_level) ** (delta_days / 50)
        
        total_scores[team_name] = total_score

    # 按总的战队积分排名
    ranked_teams = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    rankings = {team_name: i + 1 for i, (team_name, _) in enumerate(ranked_teams)}

    return total_scores, rankings

def print_multiple_files_results(results, file_data, total_scores, rankings):
    """
    输出多个文件的第五个积分表格，每个队伍名只出现一次
    增加两列：总的战队积分和排名
    """
    # 表头
    header = ["Team"] + [file_info['file_name'] for file_info in file_data] + ["Total Score", "Rank"]
    print("{:<20}".format(header[0]), end="")
    for col in header[1:]:
        print("{:<15}".format(col), end="")
    print()

    # 表格内容
    for team_name, file_scores in results.items():
        print("{:<20}".format(team_name), end="")
        for file_info in file_data:
            file_name = file_info['file_name']
            score = file_scores.get(file_name, "N/A")
            print("{:<15.4f}".format(score) if score != "N/A" else "{:<15}".format(score), end="")
        # 输出总的战队积分和排名
        print("{:<15.4f} {:<15}".format(total_scores.get(team_name, 0), rankings.get(team_name, "N/A")))

def save_multiple_files_results(results, file_data, total_scores, rankings, output_file_path):
    """
    将多个文件的第五个积分表格保存为 .csv 文件
    """
    # 表头
    header = ["Team"] + [file_info['file_name'] for file_info in file_data] + ["Total Score", "Rank"]

    # 写入 .csv 文件
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # 写入表头

        # 表格内容
        for team_name, file_scores in results.items():
            row = [team_name]
            for file_info in file_data:
                file_name = file_info['file_name']
                score = file_scores.get(file_name, "N/A")
                row.append(score if score == "N/A" else f"{score:.4f}")
            # 添加总的战队积分和排名
            row.append(f"{total_scores.get(team_name, 0):.4f}")
            row.append(rankings.get(team_name, "N/A"))

            # 写入 .csv 文件
            writer.writerow(row)

    print(f"Results saved to {output_file_path}")

def print_team_integrals(data):
    """
    输出队伍的积分表格，包含第一个积分、第二个积分、总奖励分、第三个积分、第四个积分和第五个积分
    """
    print("\nTeam Integrals and Bonus:")
    print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        "Team", "First Integral", "Second Integral", "Total Bonus", "Third Integral", "Fourth Integral", "Fifth Integral"
    ))
    for team_name, team in data['teams'].items():
        print("{:<20} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f} {:<15.4f}".format(
            team_name,
            team['first_integral'],
            team['second_integral'],
            team.get('total_bonus', 0),  # 如果总奖励分不存在，则默认为0
            team.get('third_integral', 0),  # 如果第三个积分不存在，则默认为0
            team.get('fourth_integral', 0),  # 如果第四个积分不存在，则默认为0
            team.get('fifth_integral', 0)  # 如果第五个积分不存在，则默认为0
        ))

# # #

# #主程序

# 查找队伍排名总表的程序
directory_path = r''  # 替换为你自己的 .csv 文件目录路径

# 处理多个文件
results, file_data = process_multiple_files(directory_path)

# 计算总的战队积分和排名
total_scores, rankings = calculate_total_team_score(results, file_data)

# 输出表格
print_multiple_files_results(results, file_data, total_scores, rankings)

# # 保存表格到 .csv 文件
output_file_path = os.path.join(os.getcwd(), "team_scores.csv")  # 保存路径
save_multiple_files_results(results, file_data, total_scores, rankings, output_file_path)

# # #


# # 查找单场比赛数据的程序（自己改）
# file_path = 'mate_s5.csv'  #文件名自己改，想看哪个改哪个
# data = parse_csv(file_path)
# data = calculate_first_integral(data)
# data = calculate_second_integral(data)
# data = calculate_total_bonus(data)
# data = calculate_third_integral(data)
# data = calculate_fourth_integral(data)
# data = calculate_fifth_integral(data)

# # 输出比赛日期、队伍数量和比赛等级参数
# print("Match Date:", data['date'])
# print("Number of Teams:", data['num_teams'])
# print("Competition Level:", data['competition_level'])

# # 输出队伍的积分表格
# print_team_integrals(data)

# # 获取特定队伍的统计数据
# team_name = ''  #队伍名自己改，跟.csv表格要一致
# stats = get_team_stats(data, team_name)
# if stats:
#     print(f"\nStats for {team_name}:")
#     print(stats)
# else:
#     print(f"\nTeam {team_name} not found.")