crop_variations = {
    "Winter,Wheat": ["winter wheat","winterwheat","Пшениця озима".lower()],
    "Spring,Wheat": ["spring wheat","springwheat"],
    "Sunflower": ["Соняшник".lower()],
    "Maize": ["maize","corn","corn for grain","Кукурудза на зерно".lower(),"mz"],
    "Silage,Maize" : ["silage","corn for green mass","Силос".lower(),"Кукурудза силосна".lower(),"Кукурудза на силос".lower()],
    "Barley":["barley"],
    "Spring,Barley": ["spring barley","springbarley","Ячмінь ярий".lower()],
    "Winter,Barley": ["winter barley","winterbarley","Ячмінь озимий".lower()],
    "Winter,Rye": ["winterrye","winter rye"],
    "Winter,Rapeseed": ["Ріпак озимий".lower(),"winter rapeseed"],
    "Chickpeas" : ["chickpeas","chickpea"],
    "Pigeon_Pea": ["pigeonpea","pigeon pea","pp","pigeonpeas","pigeon peas"],
    "Cowpea": ["cp","cowpeas","cow pea"],
    "Soybean": ["soy", "soybean","soybeans","sb"],
    "Groundnut" : ["gn","groundnuts","groudnuts"],
    "Apple": ["apple","Яблука".lower()],
    "Potato": ["Potatoes"],
    "Grassland" : ["Трави однорічні".lower(),"Багаторічні трави".lower(),"herbs","Однорічні трави".lower(),"bareland","Пасовище".lower(),"Пасовище".lower()],
    "Oats" : ["Віко овес".lower(),"oats"],
    "Cabbage":["cabbages"],
    "Sugar_Beet": ["sugar beet","sugarbeet","Sugar been","Sugar Beet"],
    "Strawberry":["strawberries"],
    "Finger_Millet": ["finger millet","fingermillet","finger millets","Finger millets"],
    "Bush_Bean": ["bush beans","bushbeans"],
    "Climbing_Bean": ["climbing beans","climbingbeans"],
    "Irish_Potato": ["irish potato","potato irish","irish potatoes","potatoes irish","potatoirish"],
    "Beans": ["bean","beans"],
    "Peas": ["pea"],
    "Sweet_Potato": ["sweet potato","potato sweet","sweet potatoes","Sweet potatoes"],
    "Others": ["Засмічено ВНП".lower(),"Заліснено".lower(),"Кукурудза силосна та сорго".lower(),"Кукурудза (втрати)".lower(),"Ячмінь ярий з багаторічними травами".lower(),"Не обробляється".lower(),"Не обстежено".lower(),"Заболочені (підтоплення)".lower(),"Пар".lower(),"Трави багаторічні".lower(),"mined"],
    "Abandoned": ["without culture","Without culture"]    
}

group_codes = {
    "Cereals": {"code": "01", "crops": {"Wheat": "01", "Maize": "02", "Barley": "03", "Rye": "04", "Millet": "05", "Buckwheat": "06", "Oats": "07", "Finger_Millet": "08", "Sorghum":"09"}},
    "Oilseeds": {"code": "02", "crops": {"Mustard": "01", "Sunflower": "02", "Rapeseed": "03"}},
    "Legumes/Pulses": {"code": "03", "crops": {"Chickpeas": "01", "Alfalfa": "03", "Pigeon_Pea": "04", "Cowpea": "05", "Soybean": "06", "Groundnut": "07", "Beans": "08", "Bush_Bean": "09", "Climbing_Bean": "10"}},
    "Fruits/Vegetables": {"code": "04", "crops": {"Apple": "01", "Watermelon": "02", "Grape": "03", "Strawberry": "04", "Tomato": "05", "Potato": "06", "Peas": "07", "Cabbage": "08", "Sugar_Beet": "09", "Irish_Potato": "10", "Sweet_Potato": "11"}},
    "Non Crop": {"code":"09", "crops": {"Grassland": "01", "Fallow": "02", "Water": "03", "Forest": "04", "Garden": "05", "Wetland": "06", "Artificial": "07", "Virgin": "08", "Others": "09", "Abandoned": "10"}}
}

season_codes = { "Winter": "01", "Summer": "02", "Spring": "03", "Fall": "04", "Main": "05", "Second": "06", "First Crop": "07", "Minor": "08", "Kharif": "09", "Rabi": "10", "Monsoon": "11", "Dry": "12",
               "Wet": "13"}

variation_codes = {"Silage": "01", "Temporary": "02", "Ratoon": "03"}

intercrop_codes = {"No Intercrop": "00", "Main Intercrop": "01", "Other Intercrop": "02", "No Main Intercrop": "03"}
#changed Maize_Silage to 1023, to keep the silage code different from winter/spring
crop_codes = {
    "Wheat":101, "Winter_Wheat":1011, "Spring_Wheat":1012, "Maize":102, "Maize_Silage":1023 ,"Barley":103, "Winter_Barley":1031, "Spring_Barley":1032,
    "Rye":104, "Winter_Rye":1041, "Millet":105, "Buckwheat":106, "Oats":107, 
    "Mustard":201, "Sunflower":202, "Rapeseed":203, "Winter_Rapeseed":2031, 
    "Chickpeas":301, "Alfalfa":302, "Pigeon_Pea": 303, "Cowpea": 304,"Soybean":305, "Groundnut": 306,
    "Apple": 401, "Watermelon":402, "Grape":403,
    "Strawberry":404, "Tomato":405, "Potato":406, "Peas":407, "Cabbage":408, "Sugar_Beet":409, 
    "Grassland":501, "Fallow": 502, "Water":503, "Forest":504, "Garden":505, "Wetland":506, "Artificial":507 
}

tillage_variations = {
    "Shallow_Disking": ["shallow disking"],
    "Strip_Tilling": ["Strip-Till".lower()],
    "Deep_Disking": ["deep disking"],
    "Deep_Loosening": ["deep loosening"],
    "Disking": ["Дискування".lower()],
    "Disking (5-8cm)" : ["Дискування 5-8 См".lower()],
    "Deep_Digging": ["Глибоке Рихлення".lower()],
    "Rolling": ["Коткування".lower()],
    "Cultivation": ["Культивація".lower(),"Культивацiя".lower()],
    "Harrowing": ["Боронування Посівів".lower(),"Боронування".lower()],
    "Rolling,Grinding": ["Коткування Подрібнення".lower()],
    "Plowing": ["Оранка 18-20 См".lower(),"Оранка".lower()],
    "Vertical_Tillage": ["Вертикальна Обробка Ґрунту".lower()],
    "Pre-Harvest_Harrowing": ["Боронування Досходове".lower()],
    "Inter-Row_Cultivation": ["Культивація Міжрядна".lower(),"Мiжрядн Обр".lower()],
    "Grinding": ["Подрібнення".lower()],
    "Shelling": ["Лущення".lower()],
    "Harrowing_Post-Emergence": ["Борондосходове".lower(),"Боронпiслясход".lower()],
    "Harrowing_Fallow": ["Боронування зябу".lower()],
}

database_dtypes = {
    "TEXT" : ["Crop_Group", "Crop_Season", "Crop_Variation", "Crop", "Src_id", "Variety","Provider","Season_id","Geom_id","Tillage_Type",'Input_Type',"Src_File",'Soil_Type',
              "Protect_Type", "Protect_Variety", "Protect_Machine_Tasks","Protect_Implements","Protect_Rate_Unit", "Protect_Amount_Unit",
              "Input_Implements",'Input_Machine_Tasks','Input_Variety','Input_Amount_Unit','Sow_Amount_Unit','Tillage_Machine_Tasks','Tillage_Implements','Tillage_Depth_Unit'],
    "FLOAT": ["Yield","Input_Rate","Yield_Clean",'Soil_Temp', 'Soil_Moist(70mm)', 'Soil_Moist(280mm)','Soil_Moist(1000mm)','Protect_End_Day',
              'Protect_Amount',"Protect_Rate",'Protect_Rate_Min', 'Protect_Rate_Max',
              'Sow_Row_Spacing', 'Sow_Amount', 'Sow_Rate_Unit', 'Sow_Depth','Sow_Rate',
                'Sow_Speed',"Input_Speed","Input_Amount",'Input_Rate_Unit','Input_Depth','Input_Row_Spacing','Production',
                "Est_Sow_Year","Sow_Day","Sow_Month","Sow_Year","Tillage_Day","Tillage_Month","Tillage_Year","Harvest_Day","Harvest_Month",
                 "Harvest_Year",'Input_Day', 'Input_Month','Input_Year','Input_End_Month',"Input_End_Year",'Sow_End_Day', 'Sow_End_Year'
                 ,'Input_End_Day',"Protect_Month","Protect_Day","Protect_End_Month","Protect_End_Year",'Protect_Year', 'Sow_End_Month',
                 'Tillage_End_Year', 'Tillage_End_Day', 'Tillage_End_Month','Harvest_Month',"Harvest_End_Year","Harvest_End_Day","Harvest_End_Month",
                 'Tillage_Speed','Tillage_Depth','Tillage_Depth_Max','Tillage_Depth_Min'],
    "DATETIME": ["Harvest_Date","Tillage_Date","Sow_Date","Input_Date","Protect_Date","Protect_End_Date","Input_End_Date",'Sow_End_Date','Tillage_End_Date','Harvest_End_Date'],
    "INTEGER" : []
}

target_schema_grouped = {
    "Essential": ["Crop", "Season_id", "Geom_id", "geometry", "Est_Sow_Year", "Sow_Year", "Src_id", "Provider", "Src_File"],
    
    "Crop": ["Variety", "Crop_Group", "Crop_Season", "Crop_Variation"],
        
    "Sowing": ["Sow_Date", "Sow_Amount", "Sow_Rate", "Sow_Rate_Unit", "Sow_Depth", "Sow_Row_Spacing", "Sow_Speed", "Sow_Method", "Sow_Amount_Unit", 
                 "Sow_Day", "Sow_Month",  "Sow_End_Date", "Sow_End_Day", "Sow_End_Month", "Sow_End_Year"],
    
    "Harvest": ["Harvest_Date", "Yield", "Production", "Harvest_Day", "Harvest_Month", "Harvest_Year", 
                "Harvest_End_Date", "Harvest_End_Day", "Harvest_End_Month", "Harvest_End_Year"],
    
    "Inputs (Fertilizer/etc)": ["Input_Type", "Input_Date", "Input_Amount", "Input_Rate", "Input_Rate_Unit", "Input_Amount_Unit", "Input_Depth", 
                 "Input_Row_Spacing", "Input_Speed", "Input_Implements", "Input_Machine_Tasks", "Input_Variety",
                 "Input_Day", "Input_Month", "Input_Year", "Input_End_Date", "Input_End_Month", "Input_End_Year"],
    
    "Tillage": ["Tillage_Type", "Tillage_Date", "Tillage_Depth", "Tillage_Speed", "Tillage_Machine_Tasks", "Tillage_Implements", 
                "Tillage_Depth_Unit", "Tillage_Depth_Max", "Tillage_Depth_Min",
                "Tillage_Day", "Tillage_Month", "Tillage_Year", "Tillage_End_Date", "Tillage_End_Day", "Tillage_End_Month", "Tillage_End_Year"],
    
    "Protection": ["Protect_Type", "Protect_Date", "Protect_Variety", "Protect_Amount", "Protect_Rate", "Protect_Rate_Unit", "Protect_Amount_Unit",
                   "Protect_Rate_Min", "Protect_Rate_Max", "Protect_Machine_Tasks", "Protect_Implements",
                   "Protect_Day", "Protect_Month", "Protect_Year", "Protect_End_Date", "Protect_End_Month", "Protect_End_Year"],
    
    "Soil/Env": ["Soil_Type", "Soil_Temp", "Soil_Moist(70mm)", "Soil_Moist(280mm)", "Soil_Moist(1000mm)"]
}

target_schema_grouped_temp = {
    "Essential": ["Crop", "Season_id", "Geom_id", "geometry", "Est_Sow_Year", "Sow_Year", "Src_id", "Provider", "Src_File"],
    
    "Crop": ["Variety", "Crop_Group", "Crop_Season", "Crop_Variation"],
        
    "Sowing": ["Sow_Date", "Sow_Day", "Sow_Month"],
    
    "Harvest": ["Harvest_Date", "Yield"]
}

target_schema_grouped_temp = {
    "Essential Columns": {
        "Geom_id": {
            "description": "Unique field identifier for each geometry.",
            "dtype": "string",
            "required": True
        },
        "Season_id": {
            "description": "Unique seasonal identifier: Geom_id + Sowing information",
            "dtype": "string",
            "required": True
        },
        "Sow_Year": {
            "description": "Sowing year of the crop",
            "dtype": "integer",
            "required": True
        },
        "Est_Sow_Year": {
            "description": "Esimated year assigned to all the rows where Sow_Year is not available",
            "dtype": "integer",
            "required": True
        },
        "Src_id": {
            "description": "Original field ids present in the dataset to backtrack to the raw data",
            "dtype": "string",
            "required": True
        },
        "Src_File": {
            "description": "Paths to the original files to backtrack to the raw data",
            "dtype": "string",
            "required": True
        },
        "Provider": {
            "description": "Provider name for creditation in the project",
            "dtype": "string",
            "required": True
        },
        "Crop": {
            "description": "Crop type of each field",
            "dtype": "string",
            "required": True
        },
        "geometry": {
            "description": "Crop type of each field",
            "dtype": "geometry",
            "required": True
        },
        
    },
    "Crop Columns": {
        "Variety": {
            "description": "Variety of the crop (durum,spelt,etc)",
            "dtype": "string",
            "required": True
        },
        "Crop_Season": {
            "description": "Cropping season label (Winter, Spring, etc.).",
            "dtype": "string",
            "required": False
        },
        "Crop_Group": {
            "description": "Cropping group label (Oilseeds, Cereals, etc.).",
            "dtype": "string",
            "required": False
        },
        "Crop_Variation": {
            "description": "Cropping variation label (Silage, Ratoon, etc.).",
            "dtype": "string",
            "required": False
        }, 
    },
    "Sow Columns": {
        "Sow_Date": {
            "description": "Sowing date of the crop",
            "dtype": "datetime",
            "required": False
        },
        "Sow_Day": {
            "description": "Sowing day of the crop",
            "dtype": "integer",
            "required": False
        },
        "Sow_Month": {
            "description": "Sowing month of the crop",
            "dtype": "integer",
            "required": False
        }
    },
    "Harvest Columns": {
        "Harvest_Date": {
            "description": "Harvest date of the crop",
            "dtype": "datetime",
            "required": False
        },
        "Yield": {
            "description": "Yield of the crop in ton/ha",
            "dtype": "float",
            "required": False
        }
}
}
#                                                                                                                              
#database_schema = {
#    "Crop_Info":["Crop_Type","Variety"],
#    "Observation_Info":["Year","Provider","Yield","Harv_Date","Sow_Date"],
#    "Tillage_Info":["Till_Date","Till_Type","Till_Depth","Till_Speed"],
#    "Soil_Info":["Soil_Type"],
#    "Inputs":[]
#}
