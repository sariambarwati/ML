from flask import *
import joblib


app = Flask(__name__)


def preprocess_sex(Sex):
    Sex_M = 0
    Sex_F = 0

    if Sex == 'M':
        Sex_M = 1
    elif Sex == 'F':
        Sex_F = 1

    return Sex_M, Sex_F


def preprocess_chestpain(ChestPainType):
    ChestPainType_ATA = 0
    ChestPainType_NAP = 0
    ChestPainType_ASY = 0
    ChestPainType_TA  = 0

    if ChestPainType == 'ATA':
        ChestPainType_ATA = 1
    elif ChestPainType == 'NAP':
        ChestPainType_NAP = 1
    elif ChestPainType == 'ASY':
        ChestPainType_ASY = 1
    elif ChestPainType == 'TA':
        ChestPainType_TA = 1

    return ChestPainType_ATA, ChestPainType_NAP, ChestPainType_ASY, ChestPainType_TA


def preprocess_restingecg(RestingECG):
    RestingECG_Normal = 0
    RestingECG_ST     = 0
    RestingECG_LVH    = 0

    if RestingECG == 'Normal':
        RestingECG_Normal = 1
    elif RestingECG == 'ST':
        RestingECG_ST = 1
    elif RestingECG == 'LVH':
        RestingECG_LVH = 1

    return RestingECG_Normal, RestingECG_ST, RestingECG_LVH


def preprocess_exerciseangina(ExerciseAngina):
    ExerciseAngina_N = 0
    ExerciseAngina_Y = 0

    if ExerciseAngina == 'N':
        ExerciseAngina_N = 1
    elif ExerciseAngina == 'Y':
        ExerciseAngina_Y = 1

    return ExerciseAngina_N, ExerciseAngina_Y


def preprocess_stslope(ST_Slope):
    ST_Slope_Up   = 0
    ST_Slope_Flat = 0
    ST_Slope_Down = 0

    if ST_Slope == 'Up':
        ST_Slope_Up = 1
    elif ST_Slope == 'Flat':
        ST_Slope_Flat = 1
    elif ST_Slope == 'Down':
        ST_Slope_Down = 1

    return ST_Slope_Up, ST_Slope_Flat, ST_Slope_Down


loaded_model = joblib.load('/home/heartdiseasezenius/mysite/model_classifier_rf.pkl')


@app.route("/", methods=["GET", "POST"])
def home():
    
    str_prediction = ''
    
    if request.method == "POST":

        Age         = int(request.form["Age"])
        RestingBP   = int(request.form["RestingBP"])
        Cholesterol = int(request.form["Cholesterol"])
        FastingBS   = int(request.form["FastingBS"])
        MaxHR       = int(request.form["MaxHR"])
        Oldpeak     = float(request.form["Oldpeak"])
        
        Sex_M, Sex_F = preprocess_sex(str(request.form["Sex"]))
        
        ChestPainType_ATA, ChestPainType_NAP, \
        ChestPainType_ASY, ChestPainType_TA = preprocess_chestpain(str(request.form["ChestPainType"]))
        
        RestingECG_Normal, RestingECG_ST, RestingECG_LVH = preprocess_restingecg(str(request.form["RestingECG"]))
        
        ExerciseAngina_N, ExerciseAngina_Y = preprocess_exerciseangina(str(request.form["ExerciseAngina"]))
        
        ST_Slope_Up, ST_Slope_Flat, ST_Slope_Down = preprocess_stslope(str(request.form["ST_Slope"]))
        
        
        ls_data = [Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak, \
                   Sex_F, Sex_M, \
                   ChestPainType_ASY, ChestPainType_ATA, ChestPainType_NAP, ChestPainType_TA, \
                   RestingECG_LVH, RestingECG_Normal, RestingECG_ST, \
                   ExerciseAngina_N, ExerciseAngina_Y, \
                   ST_Slope_Down, ST_Slope_Flat, ST_Slope_Up]
        
        prediction_results = loaded_model.predict([ls_data])
        prediction_results = prediction_results[0]
        
        if prediction_results == 1:
            str_prediction = 'Wah anda sakit jantung!'
        elif prediction_results == 0:
            str_prediction = 'Wah anda sehat!'

        
    return render_template("home.html", str_prediction=str_prediction)


