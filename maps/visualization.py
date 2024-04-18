def get_breaks():
    return {
        'NDWI_I': [-1.0,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0],
        'NDWI_II': [-1.0,-0.8,-0.6,-0.5,-0.4,-0.2,0.0,0.2,0.5,0.8,1.0],
        'NDVI': [-1.0,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0],
        'MSAVI2': [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0],
        'EVI': [-1.0,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0],
        'NMDI': [0.0,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,1],
        'MSI': [0.0,0.2,0.4,0.5,0.8,1.0,1.5,2.0,3.0,4.0,6.0]
    }

def get_palette():
    return {
        'NDWI_I': ["#8B0000", "#962A2A", "#A15454", "#AD7E7E", "#B8A8A8", "#ACB2B9", "#889CB0", "#6585A6", "#416E9D", "#1E5894"], #RdBl
        'NDWI_II': ["#888888", "#959595", "#B5B5B5", "#D2D2D2", "#E2E2E2", "#F4F4F4", "#9CDBF3", "#4DADDB", "#217BB6", "#1E5894"], #GyBl
        'NDVI': ["#8B0000", "#A03323", "#B66647", "#CC996B", "#E2CC8F", "#D2D790", "#9EBA6C", "#699D48", "#348024", "#006400"], #RdYlGn
        'MSAVI2': ["#CB1212", "#D24132", "#DA7051", "#E19F71", "#E9CE92", "#D2D790", "#9EBA6C", "#699D48", "#348024", "#006400"], #RdGn
        'EVI': ["#D3D3D3", "#BBC6BB", "#A4BAA4", "#8CAE8C", "#75A175", "#5D955D", "#468946", "#2E7C2E", "#177017", "#006400"], #Gn
        'NMDI_temp': ["#1E5894", "#507BA8", "#82A0BD", "#B3C3D2", "#E5E7E7", "#F2ECE4", "#D9D2C9", "#BFB7AD", "#A69D92", "#8D8377"], #BrBl
        'NMDI': ["#8D8377", "#A69D92", "#BFB7AD", "#D9D2C9", "#F2ECE4", "#E5E7E7", "#B3C3D2", "#82A0BD", "#507BA8", "#1E5894"], #BlBr
        #'MSI': ["#1E5894", "#416E9D", "#6585A6", "#889CB0", "#ACB2B9", "#B8A8A8", "#AD7E7E", "#A15454", "#962A2A", "#8B0000"] #BlRd
        'MSI': ["#5fcdd9","#59bcc7","#53aab5","#4d99a3","#478891","#40767f","#3a656d","#34545b","#2e4249","#283137"],
        'line_chart': ["#ebf7fa", "#5fcdd9", "#478891"],
        'multi_year_chart': ['#36afcc', "#4ab7d1", '#72c7db', "#afdfeb", "#0afaf6", "#d7eff5", "#ebf7fa"],
        'multi_year_histogram': "#5fcdd9",
        'changes': ["#53aab5", "#5fcdd9", "#AD7E7E",'#962A2A']
    }

def get_vis_params():
    palette = get_palette()
    breaks = get_breaks()

    vis_params = {
        'NDWI_I': {'min': 1, 'max': 10, 'palette': palette['NDWI_I'], 'breaks': breaks['NDWI_I']},
        'NDWI_II': {'min': 1, 'max': 10, 'palette': palette['NDWI_II'], 'breaks': breaks['NDWI_II']},
        'NDVI': {'min': 1, 'max': 10, 'palette': palette['NDVI'], 'breaks': breaks['NDVI']},
        'MSAVI2': {'min': 1, 'max': 10, 'palette': palette['MSAVI2'], 'breaks': breaks['MSAVI2']},
        'EVI': {'min': 1, 'max': 10, 'palette': palette['EVI'], 'breaks': breaks['EVI']},
        'NMDI': {'min': 1, 'max': 10, 'palette': palette['NMDI'], 'breaks': breaks['NMDI']},
        'MSI': {'min': 1, 'max': 10, 'palette': palette['MSI'], 'breaks': breaks['MSI']},
        'changes': {'min': 1, 'max': 4, 'palette': palette['changes']}
    }

    return vis_params

def get_labels():
    return {
        'NDWI_I': ['-1.0-0.0','0.0-0.1','0.1-0.2','0.2-0.3','0.3-0.4','0.4-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-1.0'],
        'NDWI_II': ['-1.0--0.8','-0.8--0.6','-0.6--0.5','-0.5--0.4','-0.4--0.2','-0.2-0.0','0.0-0.2','0.2-0.5','0.5-0.8','0.8-1.0'],
        'NDVI': ['-1.0--0.1','-0.1-0.1','0.1-0.2','0.2-0.3','0.3-0.4','0.4-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-1.0'],
        'MSAVI2': ['-1.0,-0.8','-0.8--0.6','-0.6--0.4','-0.4--0.2','-0.2-0.0','0.0-0.2','0.2-0.4','0.4-0.6','0.6-0.8','0.8-1.0'],
        'EVI': ['-1.0,0.0','0.0-0.1','0.1-0.2','0.2-0.3','0.3-0.4','0.4-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-1.0'],
        'NMDI': ['0.00,0.30','0.30-0.35','0.35-0.40','0.40-0.45','0.45-0.50','0.50-0.55','0.55-0.60','0.60-0.65','0.65-0.70','0.70-1.00'],
        'MSI': ['0.0-0.2', '0.2-0.4', '0.4-0.5', '0.5-0.8', '0.8-1.0', '1.0-1.5', '1.5-2.0', '2.0-3.0', '3.0-4.0', '4.0-6.0'],
        'changes': ['Strong Negative Changes', 'Negative Changes', 'Positive Changes', 'Strong Positive Changes']
    }