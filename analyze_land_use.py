import pandas as pd
import numpy as np

def analyze_land_use_types():
    """分析土地用途类型"""
    print("正在读取CSV文件...")
    
    # 分块读取大文件
    chunk_size = 10000
    land_use_counts = {}
    
    for chunk in pd.read_csv('土地出让信息（2000-2024年）.csv', chunksize=chunk_size):
        # 统计土地用途
        land_use_chunk = chunk['土地用途'].value_counts()
        for use_type, count in land_use_chunk.items():
            if use_type in land_use_counts:
                land_use_counts[use_type] += count
            else:
                land_use_counts[use_type] = count
    
    # 转换为Series并排序
    land_use_series = pd.Series(land_use_counts).sort_values(ascending=False)
    
    print(f"\n=== 土地用途类型统计（共{len(land_use_series)}种） ===")
    for use_type, count in land_use_series.items():
        print(f"{use_type}: {count:,}")
    
    return land_use_series

def identify_affordable_housing_types(land_use_series):
    """识别保障房相关的土地用途类型"""
    print("\n=== 保障房相关的土地用途类型 ===")
    
    # 保障房相关关键词
    affordable_keywords = [
        '保障', '经济适用', '廉租', '公租', '安置', '拆迁', 
        '限价', '社会保障', '人才', '公共租赁'
    ]
    
    affordable_types = []
    
    for use_type in land_use_series.index:
        if pd.isna(use_type):
            continue
        use_type_str = str(use_type)
        for keyword in affordable_keywords:
            if keyword in use_type_str:
                affordable_types.append(use_type)
                print(f"✓ {use_type}: {land_use_series[use_type]:,}")
                break
    
    return affordable_types

def filter_affordable_housing_data(affordable_types):
    """筛选保障房相关数据"""
    print(f"\n正在筛选保障房数据...")
    
    chunk_size = 10000
    affordable_data = []
    
    for chunk in pd.read_csv('土地出让信息（2000-2024年）.csv', chunksize=chunk_size):
        # 筛选保障房相关记录
        affordable_chunk = chunk[chunk['土地用途'].isin(affordable_types)]
        if not affordable_chunk.empty:
            affordable_data.append(affordable_chunk)
    
    if affordable_data:
        # 合并所有数据
        result_df = pd.concat(affordable_data, ignore_index=True)
        
        print(f"筛选出保障房相关记录: {len(result_df):,} 条")
        
        # 保存到新文件
        output_file = '保障房土地出让数据.csv'
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"数据已保存到: {output_file}")
        
        # 显示基本统计信息
        print(f"\n=== 保障房数据基本统计 ===")
        print(f"时间跨度: {result_df['年份'].min()} - {result_df['年份'].max()}")
        print(f"涉及省份: {result_df['省'].nunique()} 个")
        print(f"涉及城市: {result_df['市'].nunique()} 个")
        
        # 按年份统计
        yearly_counts = result_df['年份'].value_counts().sort_index()
        print(f"\n=== 按年份分布 ===")
        for year, count in yearly_counts.items():
            print(f"{year}: {count:,}")
        
        # 按土地用途统计
        print(f"\n=== 按土地用途分布 ===")
        use_counts = result_df['土地用途'].value_counts()
        for use_type, count in use_counts.items():
            print(f"{use_type}: {count:,}")
        
        return result_df
    else:
        print("未找到保障房相关数据")
        return None

if __name__ == "__main__":
    # 1. 分析土地用途类型
    land_use_series = analyze_land_use_types()
    
    # 2. 识别保障房相关类型
    affordable_types = identify_affordable_housing_types(land_use_series)
    
    # 3. 筛选并导出数据
    if affordable_types:
        affordable_df = filter_affordable_housing_data(affordable_types)
    else:
        print("未找到保障房相关的土地用途类型")