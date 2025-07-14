import pandas as pd

def precise_filter_affordable_housing():
    """使用精确白名单筛选保障房数据"""
    
    # 明确的保障房用途白名单
    affordable_housing_types = [
        # 经济适用房系列
        '经济适用住房用地',
        '城镇住宅-经济适用住房用地', 
        '经济适用住房用地(一类)',
        '经济适用住房用地(二类)',
        '经济适用住房用地(三类)',
        
        # 限价商品房
        '中低价位、中小套型普通商品住房用地',
        
        # 公租房系列
        '公共租赁住房用地',
        '城镇住宅-公共租赁住房用地',
        '公共租赁住房用地(一类)',
        '公共租赁住房用地(二类)', 
        '公共租赁住房用地(三类)',
        
        # 廉租房
        '廉租住房用地',
        
        # 共有产权房
        '城镇住宅-共有产权住房用地',
        '共有产权住房用地(一类)',
        '共有产权住房用地(二类)',
        '共有产权住房用地(三类)',
        
        # 安置房系列  
        '城镇住宅-用于安置的商品住房用地 ',  # 注意这里有个空格
        '用于安置的商品住房用地(一类)',
        '用于安置的商品住房用地(二类)',
        '用于安置的商品住房用地(三类)',
        
        # 保障性租赁住房
        '保障性租赁住房',
        '保障性租赁住房用地(一类)',
        '保障性租赁住房用地(二类)',
        '保障性租赁住房用地(三类)',
        
        # 配售型保障房
        '配售型保障房(一类)',
        '配售型保障房(二类)', 
        '配售型保障房(三类)',
        
        # 租赁型商品住房（人才房等）
        '城镇住宅-租赁型商品住房用地',
        '租赁型商品住房用地(一类)',
        '租赁型商品住房用地(二类)'
    ]
    
    print(f"使用白名单筛选保障房数据，共{len(affordable_housing_types)}种用途类型")
    print("\n白名单包含的用途类型：")
    for i, use_type in enumerate(affordable_housing_types, 1):
        print(f"{i:2d}. {use_type}")
    
    # 分块读取并筛选数据
    print(f"\n正在筛选保障房数据...")
    chunk_size = 50000
    affordable_data = []
    total_processed = 0
    
    for chunk in pd.read_csv('土地出让信息（2000-2024年）.csv', chunksize=chunk_size, low_memory=False):
        total_processed += len(chunk)
        
        # 使用白名单精确筛选
        affordable_chunk = chunk[chunk['土地用途'].isin(affordable_housing_types)]
        
        if not affordable_chunk.empty:
            affordable_data.append(affordable_chunk)
        
        if total_processed % 500000 == 0:
            print(f"已处理 {total_processed:,} 行数据...")
    
    print(f"数据处理完成，共处理 {total_processed:,} 行")
    
    if affordable_data:
        # 合并所有数据
        result_df = pd.concat(affordable_data, ignore_index=True)
        
        print(f"\n=== 精确筛选结果 ===")
        print(f"筛选出保障房相关记录: {len(result_df):,} 条")
        
        # 保存到新文件
        output_file = '精确筛选_保障房土地出让数据.csv'
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"数据已保存到: {output_file}")
        
        # 显示详细统计信息
        print(f"\n=== 基本统计信息 ===")
        print(f"时间跨度: {result_df['年份'].min()} - {result_df['年份'].max()}")
        print(f"涉及省份: {result_df['省'].nunique()} 个")
        print(f"涉及城市: {result_df['市'].nunique()} 个")
        
        # 按土地用途详细统计
        print(f"\n=== 按土地用途分布（详细） ===")
        use_counts = result_df['土地用途'].value_counts()
        total_count = len(result_df)
        
        for use_type, count in use_counts.items():
            percentage = (count / total_count) * 100
            print(f"{use_type}: {count:,} ({percentage:.1f}%)")
        
        # 按年份统计
        print(f"\n=== 按年份分布 ===")
        yearly_counts = result_df['年份'].value_counts().sort_index()
        for year, count in yearly_counts.items():
            print(f"{year}: {count:,}")
        
        # 按省份统计（前10）
        print(f"\n=== 按省份分布（前10） ===")
        province_counts = result_df['省'].value_counts().head(10)
        for province, count in province_counts.items():
            percentage = (count / total_count) * 100
            print(f"{province}: {count:,} ({percentage:.1f}%)")
        
        # 成交价格统计（排除0值）
        price_data = result_df[result_df['成交价格_万元'] > 0]['成交价格_万元']
        if not price_data.empty:
            print(f"\n=== 成交价格统计（万元，排除0值） ===")
            print(f"有效价格记录: {len(price_data):,} 条")
            print(f"平均价格: {price_data.mean():.2f}")
            print(f"中位数价格: {price_data.median():.2f}")
            print(f"最高价格: {price_data.max():.2f}")
            print(f"最低价格: {price_data.min():.2f}")
        
        # 供地面积统计（排除空值）
        area_data = result_df.dropna(subset=['供地面积_公顷'])['供地面积_公顷']
        if not area_data.empty:
            print(f"\n=== 供地面积统计（公顷） ===")
            print(f"有效面积记录: {len(area_data):,} 条")
            print(f"平均面积: {area_data.mean():.2f}")
            print(f"中位数面积: {area_data.median():.2f}")
            print(f"总面积: {area_data.sum():.2f}")
        
        return result_df
    else:
        print("未找到保障房相关数据")
        return None

if __name__ == "__main__":
    affordable_df = precise_filter_affordable_housing()
    
    print(f"\n=== 筛选完成 ===")
    print("精确筛选完成，可以基于这个数据进行进一步分析")