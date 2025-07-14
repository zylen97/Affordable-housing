import pandas as pd

def explore_all_land_use_types():
    """完整探索所有土地用途类型"""
    print("正在读取CSV文件并统计土地用途...")
    
    # 分块读取并统计土地用途
    chunk_size = 50000
    land_use_counts = {}
    
    for chunk in pd.read_csv('土地出让信息（2000-2024年）.csv', chunksize=chunk_size):
        land_use_chunk = chunk['土地用途'].value_counts()
        for use_type, count in land_use_chunk.items():
            if use_type in land_use_counts:
                land_use_counts[use_type] += count
            else:
                land_use_counts[use_type] = count
    
    # 转换为DataFrame便于分析
    land_use_df = pd.DataFrame(list(land_use_counts.items()), 
                              columns=['土地用途', '数量'])
    land_use_df = land_use_df.sort_values('数量', ascending=False).reset_index(drop=True)
    
    print(f"\n=== 所有土地用途类型（共{len(land_use_df)}种） ===")
    
    # 保存完整列表到文件
    land_use_df.to_csv('所有土地用途统计.csv', index=False, encoding='utf-8-sig')
    print(f"完整统计已保存到: 所有土地用途统计.csv")
    
    # 显示前50个最常见的
    print(f"\n=== 前50个最常见的土地用途 ===")
    for i, row in land_use_df.head(50).iterrows():
        print(f"{i+1:2d}. {row['土地用途']}: {row['数量']:,}")
    
    # 查找可能的住房相关用途
    print(f"\n=== 包含'住房'/'住宅'关键词的用途 ===")
    housing_related = land_use_df[
        land_use_df['土地用途'].str.contains('住房|住宅', na=False)
    ]
    for i, row in housing_related.iterrows():
        print(f"• {row['土地用途']}: {row['数量']:,}")
    
    # 查找可能的保障房相关用途
    print(f"\n=== 可能的保障房相关用途（初步筛选） ===")
    keywords = ['保障', '经济适用', '廉租', '公租', '安置', '拆迁', '限价', '人才', '公共租赁', '共有产权', '棚改', '回迁']
    potential_affordable = land_use_df[
        land_use_df['土地用途'].str.contains('|'.join(keywords), na=False)
    ]
    for i, row in potential_affordable.iterrows():
        print(f"• {row['土地用途']}: {row['数量']:,}")
    
    return land_use_df

if __name__ == "__main__":
    land_use_df = explore_all_land_use_types()
    
    print(f"\n=== 建议 ===")
    print("1. 查看 '所有土地用途统计.csv' 文件，人工审查所有用途类型")
    print("2. 根据具体用途名称，制定精准的筛选策略")
    print("3. 特别关注包含住房/住宅的用途类型")