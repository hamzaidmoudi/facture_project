from flask import Flask ,render_template, request ,redirect, session
from datetime import datetime
import pdfkit
 
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

muz=(' ','Onze', 'Douze', 'Treize',
          'Quatorze', 'Quinze', 'Seize', 'Dix-Sept', 'Dix-Huit', 'Dix-Neuf' )

to_19_fr = ( 'Zéro',  'Un',   'Deux',  'Trois', 'Quatre',   'Cinq',   'Six',
          'Sept', 'Huit', 'Neuf', 'Dix',   'Onze', 'Douze', 'Treize',
          'Quatorze', 'Quinze', 'Seize', 'Dix-Sept', 'Dix-Huit', 'Dix-Neuf' )
tens_fr  = ( 'Vingt', 'Trente', 'Quarante', 'Cinquante', 'Soixante', 'Soixante-Dix', 'Quatre-Vingt', 'Quatre-Vingt Dix')
denom_fr = ( '',
          'Mille',     'Million(s)',         'Milliards',       'Billions',       'Quadrillions',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Décillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Icosillion', 'Vigintillion' )

def _convert_nn_fr(val):
    """ convertion des valeurs < 100 en Français
    """
    if val < 20:
        return to_19_fr[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_fr)):
          if dval + 10 > val:
                if val % 10:
                      if(val>70 and val <= 79):
                           dcap='Soixante'
                           return dcap + '-' +muz[val % 10]
                      
                      if(val>90 and val <=99 ):
                            dcap='Quatre-vingt'
                            return dcap + '-' +muz[val % 10]
                      else:
                              return dcap + '-' +to_19_fr[val % 10]
                      
                
                return dcap 
def _convert_nnn_fr(val):
    """ convert a value < 1000 to french
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    b = val // 100
    if rem > 0:
         if b == 1 :
               word= 'Cent'
         else:
               word = to_19_fr[rem] + ' Cent'
    if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_fr(mod)
    return word

def french_number(val):
    if val < 100:
        return _convert_nn_fr(val)
    if val < 1000:
         return _convert_nnn_fr(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_fr))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            if (l ==1 ) and (denom_fr[didx] == 'Mille'):
                ret = denom_fr[didx]
            else:
                  ret = _convert_nnn_fr(l) + ' ' + denom_fr[didx]
            if r > 0:
                ret = ret + ' ' + french_number(r)
            return ret

def amount_to_text_fr(number):
    import math
    number = '%.2f' % number
    units_name = ' '
    list = str(number).split('.')
    muzamil=(french_number(abs(int(list[0]))))
    start_word = muzamil
    end_word =''
    #french_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and ' dirhams' or ' dirhams'
    final_result = start_word +' '+units_name+' '+ end_word +' '+cents_name
    return final_result
@app.route("/data",methods=['POST','GET'])    
def data():
    if request.method=="POST":
        if request.form["nom"] and request.form["ice"] and request.form["qte"] and request.form["puht"] and request.form["adress"] and request.form["desi"] and request.form["dtf"]:
            total=int(request.form["qte"])*int(request.form["puht"])
            ttc=total*1.2
            return render_template("data.html",nom=request.form["nom"],ice=request.form["ice"],qte=request.form["qte"],puht=request.form["puht"],total=total,tva=(total*20)/100,ttc=ttc,adress=request.form["adress"],desi=request.form["desi"],date=str(datetime.now().strftime('%Y-%m-%d')),dtf=request.form["dtf"],nbch=amount_to_text_fr(ttc))  

@app.route("/pdf")
def pdf():
    pdfkit.from_file(data(), 'out.pdf')
    return res 


if __name__== "__main__":
    app.run(debug=True)    

    