import argparse
import pandas as pd
from tqdm import tqdm
from word_typo_maker import WordTypoMaker
from sent_typo_maker import make_typo_in_sent

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file_name',
        type=str,
        default='',
        help='original data file must be located in same directory'
    )
    parser.add_argument(
        '--column_name',
        type=str,
        default='',
        help='name of the column containing the text to be augmented in the dataframe'
    )
    parser.add_argument(
        '--augment_size',
        type=int,
        default=2,
        help='decide how much to augment'
    )
    parser.add_argument(
        '--typo_ratio',
        type=float,
        default=0.5,
        help='ratio of how many words to make typo in a sentence'
    )
    parser.add_argument(
        '--strength',
        type=str,
        default='default',
        choices=['default','normal','strong'],
        help='rule of how many characters to make typo in a word'
    )
    args = parser.parse_args()
    
    
    # 데이터 불러오기 및 증강한 데이터 편하게 보기 위한 id 추가
    data = pd.read_csv(f'./{args.file_name}.txt', sep='\t')
    if 'id' not in list(data.columns):
        data['id'] = list(range(0, len(data)))
    data = data.dropna(subset=[f'{args.column_name}'], axis=0).reset_index()
        
    # augment_size만큼 기존 데이터 복제
    for _ in range(args.augment_size-1):
        append_data = pd.read_csv(f'./{args.file_name}.txt', sep='\t')
        if 'id' not in list(append_data.columns):
            append_data['id'] = list(range(0, len(append_data)))
        append_data = append_data.dropna(subset=[f'{args.column_name}'], axis=0).reset_index()
        
        data = pd.concat([data, append_data], ignore_index=True)
    data = data.sort_values('id', ignore_index=True)
    
    # 각 문장마다 오타를 활용한 데이터 증강
    word_typo_maker = WordTypoMaker()
    for i in tqdm(range(len(data))):
        # 기존 문장
        if i%args.augment_size == 0: continue

        # 오타로 추가된 문장
        sent = data.iloc[i][args.column_name]
        new_sent = make_typo_in_sent(sent, word_typo_maker,
                                     args.typo_ratio, args.strength)
        data.loc[i, args.column_name] = new_sent
        
    # 데이터 저장
    data.to_csv(f'./{args.file_name}_{args.augment_size}_{args.typo_ratio}_{args.strength}.csv',
                index=False, encoding='utf-8-sig')
    print(f'augment_size = {args.augment_size}')
    print(f'typo_ratio   = {args.typo_ratio}')
    print(f'strength     = {args.strength}')
    print(f'오타 증강 데이터셋 {args.file_name}.csv를 저장했습니다.')