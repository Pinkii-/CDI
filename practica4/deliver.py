#!/usr/bin/python3

from math import log2, ceil

def LZ77_encode(txt,s,t):
    tokens = []
    incr = 0
    for r in range(len(txt)):
        # print(tokens)
        r = r + incr
        if (r >= len(txt)):
            break

        if r-s < 0:
            searchBuffer = txt[0:r]
        else:
            searchBuffer = txt[r-s:r]    
        lookaheadBuffer = txt[r:r+t]

        offset = 0
        length = 0
        letter = lookaheadBuffer[0]

        if len(lookaheadBuffer) == 1:
            tokens.append((offset,length,letter))
            continue

        # print("searchBuffer" ,searchBuffer, "lookaheadBuffer", lookaheadBuffer)

        window = searchBuffer + lookaheadBuffer
        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offsetAux = len(searchBuffer) - rSearchBuffer
                lengthAux = 1
                while lengthAux < len(lookaheadBuffer) and window[rSearchBuffer+lengthAux] == lookaheadBuffer[lengthAux]:
                    lengthAux += 1
                if lengthAux == len(lookaheadBuffer):
                    lengthAux -= 1
                letterAux = lookaheadBuffer[lengthAux]
                
                if lengthAux > length:
                    length = lengthAux
                    offset = offsetAux
                    letter = letterAux

        incr += length
        tokens.append((offset,length,letter))

    # print(ceil(log2(s+1)),ceil(log2(t)),ceil(log2(len(set(txt)))))

    bs = ceil(log2(s+1)) + ceil(log2(t)) + ceil(log2(len(set(txt))))
    bs = (bs * len(tokens)) / len(txt)

    return bs,tokens

def LZ77_decode(tok):
    x = ""
    for offset, length, letter in tok:
        if offset == 0:
            x += letter
        else:
            for l in range(length):
                x+= x[-offset]
            x += letter
    return x

def LZSS_encode(txt,s,t,m):
    bs = 0.0
    tokens = []
    incr = 0
    for r in range(len(txt)):
        # print(tokens)
        r = r + incr
        if (r >= len(txt)):
            break

        if r-s < 0:
            searchBuffer = txt[0:r]
        else:
            searchBuffer = txt[r-s:r]    
        lookaheadBuffer = txt[r:r+t]

        offset = 0
        length = 0
        letter = lookaheadBuffer[0]

        if len(lookaheadBuffer) == 1:
            tokens.append((0,letter))
            continue

        # print("searchBuffer" ,searchBuffer, "lookaheadBuffer", lookaheadBuffer)
        window = searchBuffer + lookaheadBuffer
        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offsetAux = len(searchBuffer) - rSearchBuffer
                lengthAux = 1
                while lengthAux < len(lookaheadBuffer) and window[rSearchBuffer+lengthAux] == lookaheadBuffer[lengthAux]:
                    lengthAux += 1
                if lengthAux == len(lookaheadBuffer):
                    lengthAux -= 1
                letterAux = lookaheadBuffer[lengthAux]
                
                if lengthAux > length:
                    length = lengthAux
                    offset = offsetAux
                    letter = letterAux

        
        if length < m:
            letter = lookaheadBuffer[0]
            tokens.append((0,letter))
            bs += 1 + ceil(log2(len(set(txt))));
        else:
            incr += length-1
            tokens.append((1,offset,length))
            bs += 1 + ceil(log2(s+1)) + ceil(log2(t))
            

    # print(ceil(log2(s+1)),ceil(log2(t)),ceil(log2(len(set(txt)))))

    bs /= len(txt)

    return bs,tokens


def LZSS_decode(tok):
    x = ""
    for t in tok:
        if t[0] == 0:
            x += t[1]
        else:
            offset = t[1]
            length = t[2]
            for l in range(length):
                x+= x[-offset]
    return x


def LZ78_encode(txt):
    bs = 0.0
    tokens = []
    # dic = list(sorted(set(txt)))
    # lastPosition = len(dic)-1
    lastPosition = 0;
    dic = [""]
    dic += [None]*((2**max((ceil(log2(len(dic)))),4) - len(dic)))
   
    # print(dic, len(dic))
    # print(lastPosition, dic)

    incr = 0
    for r in range(len(txt)):
        r = r + incr
        if (r >= len(txt)):
            break

        length = 0
        i = -1
        # print(txt, "buclee")
        # print(txt[:r], txt[r:])
        for x in range(lastPosition+1):
            # print ("   ",x, len(dic), dic[x])
            if len(dic[x]) != 1 and (len(dic[x]) < length or len(dic[x]) + r > len(txt)-1):
                continue
            # print("    ha entrado")
            lengthAux = 0
            util = True
            for p in range(len(dic[x])):
                if txt[r+p] == dic[x][p]:
                    lengthAux += 1
                else:
                    util = False
                    break
            if util and lengthAux > length:
                # print (lengthAux)
                length = lengthAux
                a = txt[r+length:r+length+1]
                i = x

        if i == -1:
            i = 0
            a = txt[r]     
        # print (" la a es ", a)

        incr += length
        lastPosition += 1
        if lastPosition >= len(dic):
            dic += [None]*len(dic)
        dic[lastPosition] = txt[r:r+length+1]
        # print (dic)
        tokens.append((i,a))
        # print (tokens)

        ba = ceil(log2(len(set(txt))))
        bi = ceil(log2(len(tokens)))
        bs += ba + bi


    bs /= len(txt)

    print (dic)

    return bs, tokens

def LZ78_decode(tok):
    x = ""
    dic = [""]
    for t in tok:
        x += dic[t[0]] + t[1]
        dic.append(dic[t[0]] + t[1])

    return x

def LZW_encode(txt):
    bs = 0
    tokens = []
    dic = list(sorted(set(txt)))
    lastPosition = len(dic)-1
    dic += [None]*((2**max((ceil(log2(len(dic)))),4) - len(dic)))
   
    # print(dic, len(dic))
    # print(lastPosition, dic)

    incr = 0
    for r in range(len(txt)):
        r = r + incr
        if (r >= len(txt)):
            break

        length = 0
        i = -1
        # print(txt, "buclee")
        # print(txt[:r], txt[r:])
        for x in range(lastPosition+1):
            # print ("   ",x, len(dic), dic[x])
            if len(dic[x]) != 1 and (len(dic[x]) < length or len(dic[x]) + r > len(txt)-1):
                continue
            # print("    ha entrado")
            lengthAux = 0
            util = True
            for p in range(len(dic[x])):
                if txt[r+p] == dic[x][p]:
                    lengthAux += 1
                else:
                    util = False
                    break
            if util and lengthAux > length:
                # print (lengthAux)
                length = lengthAux
                a = txt[r+length:r+length+1]
                i = x

        # print (" la a es ", a)

        incr += length-1
        lastPosition += 1
        if lastPosition >= len(dic):
            dic += [None]*len(dic)
        dic[lastPosition] = txt[r:r+length+1]
        # print (dic)
        tokens.append((i))
        # print (tokens)

        bs += ceil(log2(len(tokens)))

    bs /= len(txt)

    return bs, list(sorted(set(txt))), tokens

def LZW_decode(dic,tok):
    x = dic[tok[0]] 
    dic += dic[tok[0]]
    # print (dic)
    for r in range(1,len(tok)):
        # print ("tok", tok[r], "dic", dic[tok[r]])
        # print (dic[len(dic)-1])
        dic[len(dic)-1] += dic[tok[r]][0]
        # print (dic[len(dic)-1])
        x += dic[tok[r]]
        dic.append(dic[tok[r]])
        # print (dic)

    return x
    


txt1 = open("yourfilename.txt","r",encoding="utf-8").read()

txt2 = "setzejutgesdunjutjatmengenfetgedunpenjat"

# txt3 = 10*"0000000001"

# txt4 = "aaaaaaaaba"
# txt4 = "abac"

# txt = "1234123412323123987"
# txt = "AABCBBABC"
txt = txt2

## LZ77

# _, tok = LZ77_encode(txt,4096,16)

# print (tok)

# print (txt)
# print(LZ77_decode(tok))

## LZSS

# _, tok = LZSS_encode(txt,16,8,2)

# print (tok)

# print (txt)
# print(LZSS_decode(tok))

## LZ78

# print(LZ78_encode(txt))

## LZW

# print()
# print(LZW_encode(txt))
# print("decoded ",LZW_decode(list(sorted(set(txt))),LZW_encode(txt)[2]) == txt)
# print("original",txt)



# txt = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres partes de su hacienda. El resto della concluían sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mesmo, y los días de entresemana se honraba con su vellorí de lo más fino. Tenía en su casa una ama que pasaba de los cuarenta, y una sobrina que no llegaba a los veinte, y un mozo de campo y plaza, que así ensillaba el rocín como tomaba la podadera. Frisaba la edad de nuestro hidalgo con los cincuenta años; era de complexión recia, seco de carnes, enjuto de rostro, gran madrugador y amigo de la caza. Quieren decir que tenía el sobrenombre de Quijada, o Quesada, que en esto hay alguna diferencia en los autores que deste caso escriben; aunque, por conjeturas verosímiles, se deja entender que se llamaba Quejana. Pero esto importa poco a nuestro cuento; basta que en la narración dél no se salga un punto de la verdad.\nEs, pues, de saber que este sobredicho hidalgo, los ratos que estaba ocioso, que eran los más del año, se daba a leer libros de caballerías, con tanta afición y gusto, que olvidó casi de todo punto el ejercicio de la caza, y aun la administración de su hacienda. Y llegó a tanto su curiosidad y desatino en esto, que vendió muchas hanegas de tierra de sembradura para comprar libros de caballerías en que leer, y así, llevó a su casa todos cuantos pudo haber dellos; y de todos, ningunos le parecían tan bien como los que compuso el famoso Feliciano de Silva, porque la claridad de su prosa y aquellas entricadas razones suyas le parecían de perlas, y más cuando llegaba a leer aquellos requiebros y cartas de desafíos, donde en muchas partes hallaba escrito: La razón de la sinrazón que a mi razón se hace, de tal manera mi razón enflaquece, que con razón me quejo de la vuestra fermosura. Y también cuando leía: ...los altos cielos que de vuestra divinidad divinamente con las estrellas os fortifican, y os hacen merecedora del merecimiento que merece la vuestra grandeza.\nCon estas razones perdía el pobre caballero el juicio, y desvelábase por entenderlas y desentrañarles el sentido, que no se lo sacara ni las entendiera el mesmo Aristóteles, si resucitara para sólo ello. No estaba muy bien con las heridas que don Belianís daba y recebía, porque se imaginaba que, por grandes maestros que le hubiesen curado, no dejaría de tener el rostro y todo el cuerpo lleno de cicatrices y señales. Pero, con todo, alababa en su autor aquel acabar su libro con la promesa de aquella inacabable aventura, y muchas veces le vino deseo de tomar la pluma y dalle fin al pie de la letra, como allí se promete; y sin duda alguna lo hiciera, y aun saliera con ello, si otros mayores y continuos pensamientos no se lo estorbaran. Tuvo muchas veces competencia con el cura de su lugar -que era hombre docto, graduado en Sigüenza-, sobre cuál había sido mejor caballero: Palmerín de Ingalaterra o Amadís de Gaula; mas maese Nicolás, barbero del mesmo pueblo, decía que ninguno llegaba al Caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.\nEn resolución, él se enfrascó tanto en su letura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio; y así, del poco dormir y del mucho leer, se le secó el celebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamentos como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles; y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas sonadas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo. Decía él que el Cid Ruy Díaz había sido muy buen caballero, pero que no tenía que ver con el Caballero de la Ardiente Espada, que de sólo un revés había partido por medio dos fieros y descomunales gigantes. Mejor estaba con Bernardo del Carpio, porque en Roncesvalles había muerto a Roldán el encantado, valiéndose de la industria de Hércules, cuando ahogó a Anteo, el hijo de la Tierra, entre los brazos. Decía mucho bien del gigante Morgante, porque, con ser de aquella generación gigantea, que todos son soberbios y descomedidos, él solo era afable y bien criado. Pero, sobre todos, estaba bien con Reinaldos de Montalbán, y más cuando le veía salir de su castillo y robar cuantos topaba, y cuando en allende robó aquel ídolo de Mahoma que era todo de oro, según dice su historia. Diera él, por dar una mano de coces al traidor de Galalón, al ama que tenía, y aun a su sobrina de añadidura.\nEn efeto, rematado ya su juicio, vino a dar en el más estraño pensamiento que jamás dio loco en el mundo; y fue que le pareció convenible y necesario, así para el aumento de su honra como para el servicio de su república, hacerse caballero andante, y irse por todo el mundo con sus armas y caballo a buscar las aventuras y a ejercitarse en todo aquello que él había leído que los caballeros andantes se ejercitaban, deshaciendo todo género de agravio, y poniéndose en ocasiones y peligros donde, acabándolos, cobrase eterno nombre y fama. Imaginábase el pobre ya coronado por el valor de su brazo, por lo menos, del imperio de Trapisonda; y así, con estos tan agradables pensamientos, llevado del estraño gusto que en ellos sentía, se dio priesa a poner en efeto lo que deseaba.\nY lo primero que hizo fue limpiar unas armas que habían sido de sus bisabuelos, que, tomadas de orín y llenas de moho, luengos siglos había que estaban puestas y olvidadas en un rincón. Limpiólas y aderezólas lo mejor que pudo, pero vio que tenían una gran falta, y era que no tenían celada de encaje, sino morrión simple; mas a esto suplió su industria, porque de cartones hizo un modo de media celada, que, encajada con el morrión, hacían una apariencia de celada entera. Es verdad que para probar si era fuerte y podía estar al riesgo de una cuchillada, sacó su espada y le dio dos golpes, y con el primero y en un punto deshizo lo que había hecho en una semana; y no dejó de parecerle mal la facilidad con que la había hecho pedazos, y, por asegurarse deste peligro, la tornó a hacer de nuevo, poniéndole unas barras de hierro por de dentro, de tal manera que él quedó satisfecho de su fortaleza; y, sin querer hacer nueva experiencia della, la diputó y tuvo por celada finísima de encaje.\nFue luego a ver su rocín, y, aunque tenía más cuartos que un real y más tachas que el caballo de Gonela, que tantum pellis et ossa fuit, le pareció que ni el Bucéfalo de Alejandro ni Babieca el del Cid con él se igualaban. Cuatro días se le pasaron en imaginar qué nombre le pondría; porque, según se decía él a sí mesmo, no era razón que caballo de caballero tan famoso, y tan bueno él por sí, estuviese sin nombre conocido; y ansí, procuraba acomodársele de manera que declarase quién había sido, antes que fuese de caballero andante, y lo que era entonces; pues estaba muy puesto en razón que, mudando su señor estado, mudase él también el nombre, y le cobrase famoso y de estruendo, como convenía a la nueva orden y al nuevo ejercicio que ya profesaba. Y así, después de muchos nombres que formó, borró y quitó, añadió, deshizo y tornó a hacer en su memoria e imaginación, al fin le vino a llamar Rocinante: nombre, a su parecer, alto, sonoro y significativo de lo que había sido cuando fue rocín, antes de lo que ahora era, que era antes y primero de todos los rocines del mundo.\nPuesto nombre, y tan a su gusto, a su caballo, quiso ponérsele a sí mismo, y en este pensamiento duró otros ocho días, y al cabo se vino a llamar don Quijote; de donde -como queda dicho- tomaron ocasión los autores desta tan verdadera historia que, sin duda, se debía de llamar Quijada, y no Quesada, como otros quisieron decir. Pero, acordándose que el valeroso Amadís no sólo se había contentado con llamarse Amadís a secas, sino que añadió el nombre de su reino y patria, por Hepila famosa, y se llamó Amadís de Gaula, así quiso, como buen caballero, añadir al suyo el nombre de la suya y llamarse don Quijote de la Mancha, con que, a su parecer, declaraba muy al vivo su linaje y patria, y la honraba con tomar el sobrenombre della.\nLimpias, pues, sus armas, hecho del morrión celada, puesto nombre a su rocín y confirmándose a sí mismo, se dio a entender que no le faltaba otra cosa sino buscar una dama de quien enamorarse; porque el caballero andante sin amores era árbol sin hojas y sin fruto y cuerpo sin alma. Decíase él a sí:\n-Si yo, por malos de mis pecados, o por mi buena suerte, me encuentro por ahí con algún gigante, como de ordinario les acontece a los caballeros andantes, y le derribo de un encuentro, o le parto por mitad del cuerpo, o, finalmente, le venzo y le rindo, ¿no será bien tener a quien enviarle presentado y que entre y se hinque de rodillas ante mi dulce señora, y diga con voz humilde y rendido: ''Yo, señora, soy el gigante Caraculiambro, señor de la ínsula Malindrania, a quien venció en singular batalla el jamás como se debe alabado caballero don Quijote de la Mancha, el cual me mandó que me presentase ante vuestra merced, para que la vuestra grandeza disponga de mí a su talante''?\n¡Oh, cómo se holgó nuestro buen caballero cuando hubo hecho este discurso, y más cuando halló a quien dar nombre de su dama! Y fue, a lo que se cree, que en un lugar cerca del suyo había una moza labradora de muy buen parecer, de quien él un tiempo anduvo enamorado, aunque, según se entiende, ella jamás lo supo, ni le dio cata dello. Llamábase Aldonza Lorenzo, y a ésta le pareció ser bien darle título de señora de sus pensamientos; y, buscándole nombre que no desdijese mucho del suyo, y que tirase y se encaminase al de princesa y gran señora, vino a llamarla Dulcinea del Toboso, porque era natural del Toboso; nombre, a su parecer, músico y peregrino y significativo, como todos los demás que a él y a sus cosas había puesto.";

# print(LZ77_encode(txt,4095, 16)[0])
# print(LZSS_encode(txt,4095, 16,3)[0])
print(LZ78_decode(LZ78_encode(txt)[1]))
# print(LZW_encode(txt)[0])