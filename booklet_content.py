# -*- coding: utf-8 -*-
"""Content for Essential Spanish — Panama retiree booklet."""

TITLE = "Essential Spanish"
SUBTITLE = "A friendly booklet for English-speaking retirees living in Panama"
TAGLINE = "You don't need to be fluent. You need to be understood."

SECTIONS = []


def add(section):
    SECTIONS.append(section)


add({
    "id": "start-here",
    "kicker": "Start here",
    "title": "How to use this booklet",
    "intro": (
        "This is not a school textbook. It is a kitchen-table guide for real life "
        "in Panama: the farmacia, the clinic, the mercado, the taxi, and the neighbor "
        "who waters your plants when you fly home to see the grandkids."
    ),
    "blocks": [
        {"type": "p", "text": (
            "Spanish looks like a mountain from far away. Up close, you only "
            "need a few paths. This booklet is those paths. Skip around. Dog-ear the "
            "pages you actually use. Nobody is giving you a quiz."
        )},
        {"type": "ol", "title": "A simple way to use it", "items": [
            "Skim the first half once so the ideas sound familiar.",
            "Save the web version on your phone. Print the phrase pages if you like paper.",
            "When you get stuck, flip to the pattern you need — not the whole book.",
            "Say the sentences out loud. Spanish gets friendlier once your mouth has practiced it.",
        ]},
        {"type": "tip", "title": "If you remember nothing else", "text": (
            "Smile. Say <es>por favor</es> and <es>gracias</es>. Use <es>usted</es> with "
            "people you don't know well. And the magic phrase: "
            "<es>Más despacio, por favor.</es> — A little slower, please."
        )},
        {"type": "panama", "title": "Panama Spanish, in one paragraph", "text": (
            "People here speak Latin American Spanish. They do not use Spain's "
            "<es>vosotros</es>. The safe word for “you” with strangers, shopkeepers, "
            "doctors, and officials is <es>usted</es>. Friends may switch to <es>tú</es> — "
            "follow their lead. And yes, the money is already in dollars. You can skip "
            "that particular headache."
        )},
        {"type": "callout", "title": "What actually trips English speakers", "text": (
            "The splits English does not make are the ones that last: two ways to say "
            "“to be” (especially <es>estar</es>), two past tenses, and little words like "
            "<es>lo</es> and <es>la</es>. Mixing up <es>ser</es> and <es>estar</es>, or "
            "using the wrong past, is what most often confuses a listener. A wrong "
            "<es>el</es> or <es>la</es> almost never does."
        )},
        {"type": "p", "text": (
            "Mistakes are allowed. Panamanians deal with visitors from everywhere, "
            "and a kind attempt almost always beats perfect silence. If someone answers "
            "you in English, take the help. You can still sneak in a "
            "<es>gracias</es> on the way out."
        )},
    ],
})

add({
    "id": "fifteen",
    "kicker": "Chapter 1",
    "title": "Fifteen sentences that do a lot of work",
    "intro": (
        "If you only learn one page, make it this one. These sentences will get you "
        "through greetings, shops, confusion, and a polite goodbye."
    ),
    "blocks": [
        {"type": "phrases", "columns": ["Spanish", "How it sounds", "English"], "rows": [
            ["Hola. Buenos días.", "OH-lah. BWEH-nohs DEE-ahs", "Hi. Good morning."],
            ["¿Cómo está usted?", "KOH-moh es-TAH oos-TED", "How are you? (polite)"],
            ["Me llamo…", "meh YAH-moh", "My name is…"],
            ["Mucho gusto.", "MOO-choh GOO-stoh", "Nice to meet you."],
            ["No hablo español muy bien.", "no AH-bloh es-pah-NYOL mwee BYEN", "I don't speak Spanish very well."],
            ["¿Habla inglés?", "AH-blah een-GLEHS", "Do you speak English?"],
            ["Más despacio, por favor.", "MAHS des-PAH-syoh por fah-VOR", "A little slower, please."],
            ["No entiendo.", "no en-TYEN-doh", "I don't understand."],
            ["¿Puede repetir, por favor?", "PWEH-deh reh-peh-TEER", "Can you repeat that, please?"],
            ["¿Me puede ayudar?", "meh PWEH-deh ah-yoo-DAR", "Can you help me?"],
            ["¿Cuánto cuesta?", "KWAHN-toh KWEH-stah", "How much does it cost?"],
            ["Quiero esto, por favor.", "KYEH-roh ES-toh por fah-VOR", "I want this, please."],
            ["¿Dónde está el baño?", "DOHN-deh es-TAH el BAH-nyoh", "Where is the bathroom?"],
            ["Me duele aquí.", "meh DWEH-leh ah-KEE", "It hurts here. (point)"],
            ["Gracias. Que le vaya bien.", "GRAH-syahs. keh leh VAH-yah BYEN", "Thank you. Take care."],
        ]},
        {"type": "tip", "title": "Pointing is a strategy", "text": (
            "Hold up the thing, the bottle, the address on your phone. "
            "<es>Esto, por favor</es> (this, please) plus a finger will carry you "
            "farther than a perfect verb chart."
        )},
    ],
})

add({
    "id": "sounds",
    "kicker": "Chapter 2",
    "title": "How Spanish sounds",
    "intro": (
        "Here is the best news in this whole booklet: Spanish is mostly phonetic. "
        "Once the sounds are in your ear, you can read a menu out loud and be close enough."
    ),
    "blocks": [
        {"type": "h2", "text": "The five vowels never really change"},
        {"type": "p", "text": (
            "English vowels wander all over the place. Spanish vowels stay home. "
            "Learn these five and a lot of words suddenly look readable."
        )},
        {"type": "table", "headers": ["Letter", "Say it like", "Example"], "rows": [
            ["a", "ah in father", "casa, Panamá"],
            ["e", "eh in bet (clear, not “ay”)", "café, mesa"],
            ["i", "ee in machine", "sí, vino"],
            ["o", "oh in go, but shorter", "hola, doctor"],
            ["u", "oo in moon", "tú, uno"],
        ]},
        {"type": "h2", "text": "The consonants that surprise English speakers"},
        {"type": "table", "headers": ["Letter", "What to do", "Example"], "rows": [
            ["h", "Always silent.", "hola = OH-lah"],
            ["j", "A strong h, from the throat.", "José, jardín"],
            ["ll / y", "In Panama, both sound like y in yes.", "calle, playa"],
            ["ñ", "ny, as in canyon.", "mañana, señor"],
            ["r", "A quick tap (like the tt in butter, American-style).", "pero, caro"],
            ["rr", "A trill. Do your best. People will still understand you.", "perro, arroz"],
            ["v / b", "Almost the same sound. Don't stress the difference.", "vaca, banco"],
            ["qu", "A k sound. The u is silent.", "qué, quiero"],
            ["c + e/i, or z", "An s sound in Panama (not the Spanish lisp).", "cielo, cerveza"],
            ["g + e/i", "Same raspy h as j.", "gente, giro"],
        ]},
        {"type": "p", "text": (
            "Two extra spelling notes: <es>gue</es> and <es>gui</es> have a silent u "
            "(<es>guitarra</es>). And <es>qué, cuál, cómo, dónde, cuándo, quién</es> "
            "take an accent when they are questions."
        )},
        {"type": "h2", "text": "Where the stress goes"},
        {"type": "ul", "items": [
            "If there is an accent mark, stress that syllable: <es>café, teléfono, Panamá</es>.",
            "No accent, and the word ends in a vowel, n, or s? Stress the second-to-last syllable: <es>casa, hablan, lunes</es>.",
            "No accent, and it ends in any other consonant? Stress the last syllable: <es>doctor, hotel, español</es>.",
        ]},
        {"type": "tip", "title": "Skip the rolled r if you have to", "text": (
            "The sound that marks you as English is usually the vowels — keep them short "
            "and pure, not “no-uh” or “day-ee.” A weak rolled <es>rr</es> almost never "
            "blocks meaning. A swallowed vowel sometimes does."
        )},
        {"type": "panama", "title": "What your ear will notice here", "text": (
            "Along the coast, a final <es>s</es> can sound soft or almost disappear. "
            "<es>Más o menos</es> might sound like “mah o meno.” You did not go deaf. "
            "That is just Panama talking — and it can hide plurals when you listen. "
            "In the highlands (Boquete, Volcán, El Valle) speech is often a bit clearer."
        )},
    ],
})

add({
    "id": "gender",
    "kicker": "Chapter 3",
    "title": "El, la, and the idea of gender",
    "intro": (
        "Every Spanish noun is masculine or feminine. There is no secret logic that "
        "makes a table masculine and a chair feminine. Learn the little word in front "
        "with the noun, the way you learned “a pair of scissors.” English speakers "
        "slip here for years — and listeners still understand them."
    ),
    "blocks": [
        {"type": "table", "headers": ["", "Masculine", "Feminine"], "rows": [
            ["the", "el (plural: los)", "la (plural: las)"],
            ["a / an", "un (plural: unos)", "una (plural: unas)"],
        ]},
        {"type": "p", "text": "A few handy patterns — not rules you must defend in court:"},
        {"type": "ul", "items": [
            "Words ending in <es>-o</es> are usually masculine: <es>el banco, el mercado, el baño</es>.",
            "Words ending in <es>-a</es> are usually feminine: <es>la casa, la farmacia, la cuenta</es>.",
            "Words ending in <es>-ción, -sión, -dad, -tad</es> are feminine: <es>la dirección, la ciudad</es>.",
            "When in doubt, English speakers default to masculine. The slips that last are almost always on feminine words. Learn <es>la</es> with those nouns and you cut the problem in half.",
        ]},
        {"type": "h2", "text": "Professions: el and la tell you who"},
        {"type": "p", "text": (
            "Some job words don't change at all. The little word in front is the gender: "
            "<es>el</es> for a man, <es>la</es> for a woman. This is the usual pattern for "
            "words ending in <es>-ista</es>."
        )},
        {"type": "pairs", "items": [
            ["el dentista / la dentista", "the dentist (a man / a woman)"],
            ["el recepcionista / la recepcionista", "the receptionist"],
            ["el especialista / la especialista", "the specialist"],
        ]},
        {"type": "p", "text": (
            "Other jobs do change the ending: <es>el médico / la médica</es>, "
            "<es>el vecino / la vecina</es>. Either way, listen for <es>el</es> or "
            "<es>la</es> — that is who they are."
        )},
        {"type": "h2", "text": "Learn these with the article"},
        {"type": "p", "text": (
            "These are the ones that do not follow the -o / -a hint. Photograph this list."
        )},
        {"type": "table", "headers": ["Say it this way", "Why it tricks you"], "rows": [
            ["el día", "ends in -a, still masculine"],
            ["el mapa", "ends in -a, still masculine"],
            ["el problema / el clima", "the -ma words are usually masculine"],
            ["el sistema / el programa", "same -ma pattern"],
            ["el agua", "feminine, but takes el so you don't get “la agua”"],
            ["la mano", "ends in -o, still feminine"],
            ["la foto / la radio / la moto", "short for fotografía, etc. — still feminine"],
            ["el sofá", "looks like -a; masculine"],
        ]},
        {"type": "h2", "text": "Making words plural"},
        {"type": "table", "headers": ["If it ends in…", "Do this", "Example"], "rows": [
            ["a vowel", "add s", "casa to casas, taxi to taxis"],
            ["a consonant", "add es", "doctor to doctores, hotel to hoteles"],
            ["z", "change z to c, add es", "lápiz to lápices"],
        ]},
        {"type": "pairs", "title": "You'll use these every week", "items": [
            ["el médico / la médica", "the doctor"],
            ["la clínica / el hospital", "the clinic / the hospital"],
            ["la farmacia", "the pharmacy"],
            ["el mercado / el supermercado", "the market / the supermarket"],
            ["la cuenta", "the bill (or the account)"],
            ["el dinero / la plata", "money (plata is the casual word)"],
            ["el vecino / la vecina", "the neighbor"],
            ["el apartamento / la casa", "the apartment / the house"],
            ["la luz / el agua / el internet", "the power / the water / the internet"],
            ["el aire (acondicionado)", "the air conditioning"],
        ]},
        {"type": "tip", "title": "Don't wait for perfect gender", "text": (
            "If you say <es>el farmacia</es> by accident, the pharmacist will still sell you "
            "the aspirin. Listeners almost never get lost over a wrong <es>el</es> or <es>la</es>. "
            "Get the noun out. Gender can catch up later."
        )},
    ],
})

add({
    "id": "adjectives",
    "kicker": "Chapter 4",
    "title": "Describing things",
    "intro": (
        "Adjectives have to match the noun: masculine or feminine, singular or plural. "
        "And they usually come after the noun, which feels backwards until it doesn't."
    ),
    "blocks": [
        {"type": "pairs", "items": [
            ["una casa grande", "a big house"],
            ["un café bueno", "a good coffee"],
            ["las islas bonitas", "the pretty islands"],
            ["el banco está cerrado", "the bank is closed"],
        ]},
        {"type": "ul", "items": [
            "Ends in <es>-o</es>: <es>alto</es> (masculine), <es>alta</es> (feminine), <es>altos / altas</es> (plural).",
            "Ends in <es>-e</es> or a consonant: same word for masculine and feminine. Only the plural changes: <es>grande / grandes</es>, <es>fácil / fáciles</es>.",
        ]},
        {"type": "table", "headers": ["Spanish", "English"], "rows": [
            ["bueno / buena", "good"],
            ["malo / mala", "bad"],
            ["grande", "big"],
            ["pequeño / pequeña", "small"],
            ["caro / cara", "expensive"],
            ["barato / barata", "cheap"],
            ["cerca / lejos", "near / far"],
            ["caliente / frío", "hot / cold"],
            ["abierto / cerrado", "open / closed"],
            ["ocupado / libre", "busy or occupied / free"],
            ["rico / rica", "delicious (food) or rich"],
            ["limpio / sucio", "clean / dirty"],
        ]},
        {"type": "tip", "title": "Bueno likes to jump in front", "text": (
            "You'll hear <es>un buen médico</es> and <es>un mal día</es>. "
            "<es>Bueno</es> and <es>malo</es> often drop the <es>-o</es> and hop in front "
            "of a masculine noun. Copy what you hear."
        )},
    ],
})

add({
    "id": "pronouns",
    "kicker": "Chapter 5",
    "title": "I, you, we",
    "intro": (
        "Spanish has more words for “you” than English. In Panama the map is simpler "
        "than in Spain, and <es>usted</es> will keep you out of trouble."
    ),
    "blocks": [
        {"type": "table", "headers": ["Spanish", "English", "When to use it"], "rows": [
            ["yo", "I", "Talking about yourself. Often dropped: <es>Hablo inglés.</es>"],
            ["tú", "you (friendly)", "Friends, once they use tú with you."],
            ["usted", "you (polite)", "Your default. Shops, clinics, new people, anyone older."],
            ["él / ella", "he / she", "About someone else."],
            ["nosotros / nosotras", "we", "Nosotras if the group is all women."],
            ["ustedes", "you all", "Any group. Panama does not use vosotros."],
            ["ellos / ellas", "they", "Ellas if the group is all women."],
        ]},
        {"type": "panama", "title": "Usted is not stiff here", "text": (
            "In some countries <es>usted</es> can sound very formal. In Panama it is "
            "everyday respect. Using it with a cashier or a doctor is not cold — it is "
            "polite. If a neighbor switches to <es>tú</es>, you can switch too."
        )},
        {"type": "p", "text": (
            "You will notice people skip <es>yo</es> and <es>tú</es> a lot. The verb "
            "ending already says who is doing the action. <es>Tengo una cita</es> is "
            "enough. You do not need <es>Yo tengo una cita</es> unless you want to "
            "emphasize I."
        )},
        {"type": "h2", "text": "This, that, these, those"},
        {"type": "table", "headers": ["Near you", "A little farther", "A thing / idea"], "rows": [
            ["este / esta (this)", "ese / esa (that)", "esto (this thing)"],
            ["estos / estas (these)", "esos / esas (those)", "eso (that thing)"],
        ]},
        {"type": "pairs", "items": [
            ["¿Cuánto cuesta esto?", "How much is this?"],
            ["Quiero esa, por favor.", "I want that one, please."],
            ["Estos son mis medicamentos.", "These are my medicines."],
        ]},
    ],
})

add({
    "id": "ser-estar",
    "kicker": "Chapter 6",
    "title": "Two ways to say “to be”",
    "intro": (
        "English has one “to be.” Spanish has two: <es>ser</es> and <es>estar</es>. "
        "English speakers grab <es>ser</es> first and overuse it for years. "
        "The work is <es>estar</es> — especially for how someone feels and whether "
        "something is open, closed, ready, or broken."
    ),
    "blocks": [
        {"type": "h2", "text": "Ser — what something is (this one comes naturally)"},
        {"type": "p", "text": (
            "Use <es>ser</es> for identity, origin, occupation, time, dates, and "
            "the stuff something is made of. If it answers “what is it?” or “who is it?”, "
            "you probably want <es>ser</es>."
        )},
        {"type": "pairs", "items": [
            ["Soy de Canadá. / Soy de los Estados Unidos.", "I'm from Canada. / I'm from the United States."],
            ["Soy jubilado / jubilada.", "I'm retired. (that's who you are)"],
            ["Ella es médica.", "She is a doctor."],
            ["Somos vecinos.", "We're neighbors."],
            ["Es el martes. / Son las tres.", "It's Tuesday. / It's three o'clock."],
            ["El anillo es de oro.", "The ring is made of gold."],
            ["¿Quién es? — Es el plomero.", "Who is it? — It's the plumber."],
        ]},
        {"type": "h2", "text": "Estar — how or where something is (practice this one)"},
        {"type": "p", "text": (
            "Location is always <es>estar</es>, even if the place never moves: "
            "<es>Panamá está en Centroamérica.</es> Feelings, health, and “how is it "
            "right now?” are <es>estar</es> too. That last group is where English "
            "speakers keep using <es>ser</es> by accident."
        )},
        {"type": "pairs", "items": [
            ["Estoy en David. / Estamos en la capital.", "I'm in David. / We're in Panama City."],
            ["¿Cómo está usted? — Estoy bien.", "How are you? — I'm well."],
            ["Estoy cansado / cansada. Estoy enfermo / enferma.", "I'm tired. I'm sick."],
            ["El banco está cerrado. La farmacia está abierta.", "The bank is closed. The pharmacy is open."],
            ["El baño está ocupado. / Está listo.", "The bathroom is occupied. / It's ready."],
            ["La sopa está caliente. El aire no está frío.", "The soup is hot (right now). The A/C isn't cold."],
            ["Está lloviendo.", "It's raining."],
        ]},
        {"type": "callout", "title": "The mix-up that actually confuses people", "text": (
            "A wrong <es>el</es> or <es>la</es> rarely blocks meaning. Picking the wrong "
            "“to be” often does. <es>Soy enfermo</es> sounds like “I am a sick person by nature.” "
            "<es>Estoy enfermo</es> is “I'm sick (right now).” "
            "<es>Soy jubilado</es> is your identity."
        )},
        {"type": "table", "headers": ["ser", "estar"], "col_widths": [1, 1], "rows": [
            ["soy", "estoy"],
            ["eres (tú) / es (usted, él, ella)", "estás / está"],
            ["somos", "estamos"],
            ["son (ustedes, ellos, ellas)", "están"],
        ]},
        {"type": "tip", "title": "A pocket rule", "text": (
            "<es>Ser</es> = what it is. <es>Estar</es> = how or where it is right now. "
            "If you can add “at the moment” in English, try <es>estar</es>."
        )},
        {"type": "h2", "text": "Hay — there is / there are"},
        {"type": "p", "text": (
            "One more cousin: <es>hay</es> (sounds like “eye”). It means there is or "
            "there are. It does not change for plural. Mixing up <es>hay</es> with "
            "<es>es</es> or <es>está</es> is another mix-up listeners actually feel."
        )},
        {"type": "pairs", "items": [
            ["Hay un banco cerca.", "There is a bank nearby."],
            ["¿Hay una farmacia por aquí?", "Is there a pharmacy around here?"],
            ["No hay problema.", "No problem. (you'll hear this all day)"],
            ["Hay mucha gente.", "There are a lot of people."],
        ]},
        {"type": "callout", "title": "Hay vs. está", "text": (
            "<es>Hay un banco en la esquina</es> introduces it — there is a bank. "
            "<es>El banco está en la esquina</es> locates a bank you both already have in mind. "
            "If you are asking whether something exists nearby, start with <es>¿Hay…?</es>"
        )},
    ],
})

add({
    "id": "present",
    "kicker": "Chapter 7",
    "title": "Right now: the present tense",
    "intro": (
        "If you get comfortable in the present, you can handle most of a regular day. "
        "Tomorrow and yesterday can piggyback on it, as you'll see in a few chapters."
    ),
    "blocks": [
        {"type": "p", "text": (
            "Spanish verbs in the dictionary end in <es>-ar</es>, <es>-er</es>, or "
            "<es>-ir</es>. You knock that ending off and add a new one. "
            "<es>Usted</es> uses the same ending as he/she. <es>Ustedes</es> uses "
            "the same ending as they. That cuts the chart almost in half."
        )},
        {"type": "h2", "text": "hablar — to speak"},
        {"type": "table", "headers": ["Person", "Form"], "rows": [
            ["yo", "hablo"],
            ["tú", "hablas"],
            ["usted / él / ella", "habla"],
            ["nosotros", "hablamos"],
            ["ustedes / ellos / ellas", "hablan"],
        ]},
        {"type": "h2", "text": "comer — to eat"},
        {"type": "table", "headers": ["Person", "Form"], "rows": [
            ["yo", "como"],
            ["tú", "comes"],
            ["usted / él / ella", "come"],
            ["nosotros", "comemos"],
            ["ustedes / ellos / ellas", "comen"],
        ]},
        {"type": "h2", "text": "vivir — to live"},
        {"type": "table", "headers": ["Person", "Form"], "rows": [
            ["yo", "vivo"],
            ["tú", "vives"],
            ["usted / él / ella", "vive"],
            ["nosotros", "vivimos"],
            ["ustedes / ellos / ellas", "viven"],
        ]},
        {"type": "pairs", "items": [
            ["Hablo un poco de español.", "I speak a little Spanish."],
            ["¿Habla inglés?", "Do you speak English? (usted)"],
            ["Vivimos en Coronado.", "We live in Coronado."],
            ["Ellos comen a las dos.", "They eat at two."],
        ]},
        {"type": "p", "text": (
            "The present also covers things you do in general, not only this second: "
            "<es>Tomo café por la mañana.</es> I drink coffee in the morning."
        )},
        {"type": "tip", "title": "Need a verb in a hurry?", "text": (
            "You can often skip conjugating altogether: "
            "<es>Quiero + a verb</es>, <es>Necesito + a verb</es>, "
            "<es>Voy a + a verb</es>. Chapter 10 is built on that trick."
        )},
    ],
})

add({
    "id": "daily-verbs",
    "kicker": "Chapter 8",
    "title": "The verbs you'll live on",
    "intro": (
        "A short list of slightly irregular verbs does more daily work than twenty "
        "perfectly regular ones. Learn these in the present and you will hear them everywhere."
    ),
    "blocks": [
        {"type": "table", "headers": ["Infinitive", "yo", "usted / él / ella", "nosotros", "ustedes"], "rows": [
            ["ser (to be)", "soy", "es", "somos", "son"],
            ["estar (to be)", "estoy", "está", "estamos", "están"],
            ["ir (to go)", "voy", "va", "vamos", "van"],
            ["tener (to have)", "tengo", "tiene", "tenemos", "tienen"],
            ["hacer (to do / make)", "hago", "hace", "hacemos", "hacen"],
            ["poder (to be able / can)", "puedo", "puede", "podemos", "pueden"],
            ["querer (to want)", "quiero", "quiere", "queremos", "quieren"],
            ["decir (to say / tell)", "digo", "dice", "decimos", "dicen"],
            ["venir (to come)", "vengo", "viene", "venimos", "vienen"],
            ["dar (to give)", "doy", "da", "damos", "dan"],
            ["ver (to see)", "veo", "ve", "vemos", "ven"],
            ["saber (to know a fact)", "sé", "sabe", "sabemos", "saben"],
        ]},
        {"type": "p", "text": (
            "The <es>tú</es> forms (if a friend is using tú with you) usually look like "
            "the usted form plus an <es>s</es>: <es>vas, tienes, puedes, quieres</es>. "
            "Exceptions you already know: <es>eres, estás</es>."
        )},
        {"type": "h2", "text": "Tener is bigger than “to have”"},
        {"type": "p", "text": (
            "English says “I am hungry.” Spanish says “I have hunger.” Copy these as chunks."
        )},
        {"type": "pairs", "items": [
            ["Tengo hambre. / Tengo sed.", "I'm hungry. / I'm thirsty."],
            ["Tengo calor. / Tengo frío.", "I'm hot. / I'm cold."],
            ["Tengo sueño.", "I'm sleepy."],
            ["Tengo X años.", "I am X years old."],
            ["Tengo una cita a las diez.", "I have an appointment at ten."],
            ["¿Tiene cambio?", "Do you have change?"],
        ]},
        {"type": "h2", "text": "Saber vs. conocer — two kinds of knowing"},
        {"type": "pairs", "items": [
            ["¿Sabe dónde está el hospital?", "Do you know where the hospital is? (a fact)"],
            ["No sé.", "I don't know."],
            ["¿Conoce a un buen dentista?", "Do you know a good dentist? (are you familiar with one)"],
            ["Conocemos Boquete.", "We know Boquete. (we've been there)"],
        ]},
        {"type": "panama", "title": "Hace calor — and then some", "text": (
            "Weather uses <es>hacer</es>: <es>Hace calor. Hace sol. Está lloviendo.</es> "
            "In Panama, <es>verano</es> is the dry season (roughly December to April) and "
            "<es>invierno</es> is the rainy season. Nobody here is talking about snow."
        )},
    ],
})

add({
    "id": "gustar",
    "kicker": "Chapter 9",
    "title": "I like it — the gustar twist",
    "intro": (
        "<es>Gustar</es> is not “I like.” It is closer to “it is pleasing to me.” "
        "That is why the verb agrees with the thing you like, not with you. Weird for "
        "about a week. Then it clicks."
    ),
    "blocks": [
        {"type": "pairs", "items": [
            ["Me gusta el café.", "I like coffee. (one thing: gusta)"],
            ["Me gustan las empanadas.", "I like empanadas. (plural: gustan)"],
            ["No me gusta el ruido.", "I don't like the noise."],
            ["¿Le gusta el pescado?", "Do you like fish? (usted)"],
            ["Nos gusta Panamá.", "We like Panama."],
        ]},
        {"type": "table", "headers": ["Word", "English"], "rows": [
            ["me", "to me"],
            ["te", "to you (tú)"],
            ["le", "to you (usted) / to him / to her"],
            ["nos", "to us"],
            ["les", "to you all / to them"],
        ]},
        {"type": "p", "text": (
            "Want to make it extra clear? Add a phrase up front: "
            "<es>A mí me gusta…</es> <es>A usted le gusta…</es> "
            "You'll hear that a lot when people contrast tastes."
        )},
        {"type": "tip", "title": "Don't say yo gusto", "text": (
            "English wants “I like.” Spanish will not take <es>Yo gusto el café.</es> "
            "Start with <es>me</es>: <es>Me gusta el café.</es> Same family: "
            "<es>Me duele aquí. Me encanta este lugar. Me falta dinero.</es>"
        )},
        {"type": "p", "text": (
            "Love it? Same pattern: <es>Me encanta este lugar.</es> <es>Me encantan las islas.</es> "
            "That is the friendly way to say “I love it” about food, towns, and weather — "
            "not usually about people. For people, <es>Quiero mucho a…</es> is safer."
        )},
    ],
})

add({
    "id": "questions",
    "kicker": "Chapter 10",
    "title": "Questions, “no,” and the magic five",
    "intro": (
        "You can live a long time on questions, a well-placed <es>no</es>, and five "
        "little helper verbs. This chapter is the Swiss Army knife."
    ),
    "blocks": [
        {"type": "h2", "text": "Asking questions"},
        {"type": "p", "text": (
            "Written Spanish uses two question marks: <es>¿ … ?</es> Spoken Spanish "
            "often just uses tone. You can turn many statements into questions by lifting "
            "your voice: <es>¿Habla inglés?</es>"
        )},
        {"type": "table", "headers": ["Word", "English", "Try this"], "rows": [
            ["qué", "what", "¿Qué es esto?"],
            ["quién", "who", "¿Quién es?"],
            ["dónde", "where", "¿Dónde está el baño?"],
            ["cuándo", "when", "¿Cuándo abre?"],
            ["cómo", "how", "¿Cómo está usted?"],
            ["cuánto / cuánta", "how much", "¿Cuánto cuesta?"],
            ["cuántos / cuántas", "how many", "¿Cuántos años tiene?"],
            ["por qué", "why", "¿Por qué está cerrado?"],
            ["cuál", "which / what (choice)", "¿Cuál es su dirección?"],
            ["a qué hora", "at what time", "¿A qué hora es la cita?"],
        ]},
        {"type": "h2", "text": "Saying no"},
        {"type": "p", "text": (
            "Put <es>no</es> right before the verb: <es>No hablo español muy bien.</es> "
            "Double negatives are correct, not sloppy: <es>No tengo nada.</es> "
            "(I don't have anything.) <es>No hay nadie.</es> (There's no one.)"
        )},
        {"type": "pairs", "items": [
            ["No entiendo.", "I don't understand."],
            ["No sé.", "I don't know."],
            ["No, gracias.", "No, thank you."],
            ["Todavía no.", "Not yet."],
        ]},
        {"type": "h2", "text": "The magic five: want, can, need, have to, going to"},
        {"type": "p", "text": (
            "Park a verb in its dictionary form after one of these, and you can talk "
            "about almost any action without conjugating the second verb. This is the "
            "cheat that fluent-looking beginners actually use."
        )},
        {"type": "table", "headers": ["Pattern", "Example", "English"], "rows": [
            ["Quiero + verb", "Quiero pagar.", "I want to pay."],
            ["Puedo / ¿Puede…?", "¿Puede ayudarme?", "Can you help me?"],
            ["Necesito + verb", "Necesito hablar con el médico.", "I need to talk to the doctor."],
            ["Tengo que + verb", "Tengo que ir al banco.", "I have to go to the bank."],
            ["Voy a + verb", "Voy a llamar mañana.", "I'm going to call tomorrow."],
        ]},
        {"type": "pairs", "items": [
            ["Quiero reservar una mesa.", "I want to reserve a table."],
            ["No puedo caminar mucho.", "I can't walk very far."],
            ["Necesito un taxi.", "I need a taxi."],
            ["Tenemos que esperar.", "We have to wait."],
            ["Vamos a comer aquí.", "We're going to eat here."],
            ["¿Me puede escribir eso, por favor?", "Can you write that down for me, please?"],
        ]},
        {"type": "callout", "title": "Your future tense, for now", "text": (
            "Spanish has a “real” future tense (<es>hablaré, irá</es>). You can ignore it "
            "for months. <es>Voy a…</es> is what people actually say about later today, "
            "tomorrow, and next Tuesday."
        )},
    ],
})

add({
    "id": "past",
    "kicker": "Chapter 11",
    "title": "Yesterday, without the headache",
    "intro": (
        "Spanish has two everyday past tenses. English has one. That is why this "
        "chapter lasts for years. You need a snapshot version: one past for finished "
        "events, one past for background and “used to.” The English trap is using the "
        "snapshot past for both."
    ),
    "blocks": [
        {"type": "h2", "text": "The snapshot: something finished"},
        {"type": "p", "text": (
            "Use this when the thing happened and it's done. Yesterday. This morning. "
            "Last Tuesday. A completed trip to the clinic."
        )},
        {"type": "pairs", "items": [
            ["Ayer fui al médico.", "Yesterday I went to the doctor."],
            ["Comí pescado.", "I ate fish."],
            ["Pagamos en efectivo.", "We paid in cash."],
            ["¿Qué pasó?", "What happened?"],
        ]},
        {"type": "p", "text": "A few high-value “I / he-she-you” forms:"},
        {"type": "table", "headers": ["Verb", "yo", "usted / él / ella"], "rows": [
            ["ir / ser (to go / to be)", "fui", "fue"],
            ["estar", "estuve", "estuvo"],
            ["tener", "tuve", "tuvo"],
            ["hacer", "hice", "hizo"],
            ["decir", "dije", "dijo"],
            ["venir", "vine", "vino"],
            ["ver", "vi", "vio"],
            ["poder", "pude", "pudo"],
            ["dar", "di", "dio"],
            ["hablar (regular -ar)", "hablé", "habló"],
            ["comer (regular -er)", "comí", "comió"],
        ]},
        {"type": "h2", "text": "The background: how things were"},
        {"type": "p", "text": (
            "Use this for weather, age, feelings, what something used to be like, or "
            "what was going on around the main event."
        )},
        {"type": "pairs", "items": [
            ["Hacía mucho calor.", "It was really hot."],
            ["Cuando vivíamos en Florida…", "When we used to live in Florida…"],
            ["Era médico.", "He was a doctor. (that was his profession)"],
            ["Estaba cansada.", "She was tired."],
            ["Había mucha gente.", "There were a lot of people."],
        ]},
        {"type": "table", "headers": ["Useful background forms", "English"], "rows": [
            ["era / eran", "was / were (ser)"],
            ["estaba / estaban", "was / were (estar)"],
            ["había", "there was / there were"],
            ["tenía", "had / used to have"],
            ["hacía", "was making / weather was"],
            ["iba", "was going / used to go"],
            ["vivía", "used to live / was living"],
        ]},
        {"type": "h2", "text": "The English trap"},
        {"type": "p", "text": (
            "If you can add “used to” or “was …-ing” in English, do not use the snapshot "
            "past. <es>Comí pescado</es> is “I ate fish (and I was done).” "
            "<es>Comía pescado</es> is “I used to eat fish / I was eating fish.” "
            "English speakers keep putting the snapshot where the background belongs. "
            "Listeners feel that one."
        )},
        {"type": "pairs", "items": [
            ["Ayer comí pescado.", "Yesterday I ate fish. (done)"],
            ["Cuando vivía en Florida, comía pescado.", "When I lived in Florida, I used to eat fish."],
            ["Fui al médico el martes.", "I went to the doctor on Tuesday. (that visit)"],
            ["Iba al médico cada mes.", "I used to go to the doctor every month."],
        ]},
        {"type": "tip", "title": "If you freeze, tell the story in two strokes", "text": (
            "Background first, snapshot second: <es>Estaba en la casa y se fue la luz.</es> "
            "I was at the house and the power went out. That pattern will carry a lot of stories."
        )},
    ],
})

add({
    "id": "commands",
    "kicker": "Chapter 12",
    "title": "Please do this: commands",
    "intro": (
        "You don't need the full command system. You need a short list for clinics, "
        "shops, and friends. Use the <es>usted</es> column with people you don't know "
        "well. Use the <es>tú</es> column once someone is using tú with you."
    ),
    "blocks": [
        {"type": "table", "emphasis": "two-es", "headers": ["Formal (usted)", "Informal (tú)", "English"], "rows": [
            ["Deme…, por favor.", "Dame…, por favor.", "Give me…, please."],
            ["Tráigame la cuenta.", "Tráeme la cuenta.", "Bring me the bill."],
            ["Ayúdeme, por favor.", "Ayúdame, por favor.", "Help me, please."],
            ["Espere un momento.", "Espera un momento.", "Wait a moment."],
            ["Pase, por favor.", "Pasa, por favor.", "Come in, please."],
            ["Sígame, por favor.", "Sígueme, por favor.", "Follow me, please."],
            ["Hable más despacio.", "Habla más despacio.", "Speak more slowly."],
            ["Escríbalo, por favor.", "Escríbelo, por favor.", "Write it down, please."],
            ["Perdóneme.", "Perdóname.", "Excuse me / forgive me."],
            ["Dígame.", "Dime.", "Tell me."],
        ]},
        {"type": "p", "text": "You'll hear these said to you:"},
        {"type": "table", "emphasis": "two-es", "headers": ["Formal (usted)", "Informal (tú)", "English"], "rows": [
            ["Tome asiento.", "Toma asiento.", "Have a seat."],
            ["Firme aquí.", "Firma aquí.", "Sign here."],
            ["Espere aquí.", "Espera aquí.", "Wait here."],
            ["Pase a la caja.", "Pasa a la caja.", "Go to the cashier."],
            ["No fume.", "No fumes.", "No smoking. / Don't smoke."],
            ["Siéntese, por favor.", "Siéntate, por favor.", "Please sit down."],
        ]},
        {"type": "callout", "title": "How they're built, if you're curious", "text": (
            "<es>Usted</es>: start with the <es>yo</es> form in the present, drop the "
            "<es>-o</es>, and add the “opposite” vowel — <es>hablo</es> to <es>hable</es>, "
            "<es>como</es> to <es>coma</es>, <es>vivo</es> to <es>viva</es>. Rebels: "
            "<es>tenga, venga, diga, haga, ponga, vaya, sea, esté, dé</es>. "
            "<es>Tú</es> yes-commands are usually the he/she present: <es>habla, come, vive</es>. "
            "Rebels: <es>di, haz, ve, pon, sal, sé, ten, ven</es>. "
            "<es>Tú</es> no-commands look like usted plus an <es>s</es>: <es>no fumes, no hables</es>."
        )},
        {"type": "panama", "title": "Regáleme un vaso de agua", "text": (
            "You will hear <es>regalar</es> used for “hand me / give me,” not only for "
            "birthday presents. <es>¿Me regala una bolsa?</es> is a normal way to ask "
            "for a bag at the checkout. With a friend: <es>Regálame una bolsa.</es> "
            "They are not asking you to donate one."
        )},
    ],
})

add({
    "id": "por-para",
    "kicker": "Chapter 13",
    "title": "Por and para — the short version",
    "intro": (
        "Both can translate as “for,” which is unhelpful. You do not need every textbook "
        "list. You need two jobs for <es>para</es> and three jobs for <es>por</es>."
    ),
    "blocks": [
        {"type": "h2", "text": "Para — purpose, destination, deadline, recipient"},
        {"type": "pairs", "items": [
            ["Este café es para usted.", "This coffee is for you."],
            ["Salimos para Boquete el viernes.", "We're leaving for Boquete on Friday."],
            ["Lo necesito para mañana.", "I need it by tomorrow."],
            ["Estudio para hablar mejor.", "I study in order to speak better."],
        ]},
        {"type": "h2", "text": "Por — reason, duration, through, exchange"},
        {"type": "pairs", "items": [
            ["Gracias por su ayuda.", "Thank you for your help."],
            ["Caminamos por la playa.", "We walked along the beach."],
            ["Estuve allí por tres días.", "I was there for three days."],
            ["Pagué diez dólares por esto.", "I paid ten dollars for this."],
            ["Por la mañana / por la tarde / por la noche", "in the morning / afternoon / evening"],
        ]},
        {"type": "tip", "title": "Stuck?", "text": (
            "If it means “in order to,” “by this date,” “headed to,” or “this is for that person,” "
            "try <es>para</es>. If it means “because of,” “through,” “for a stretch of time,” "
            "or “in exchange for,” try <es>por</es>. And memorize <es>por favor</es> as a chunk. "
            "Do not take it apart."
        )},
    ],
})

add({
    "id": "location",
    "kicker": "Chapter 14",
    "title": "Where things are",
    "intro": (
        "Location is <es>estar</es> plus a little preposition. Learn the cluster below "
        "and you can follow directions — or give them with your hands."
    ),
    "blocks": [
        {"type": "table", "headers": ["Spanish", "English"], "rows": [
            ["en", "in / on / at"],
            ["a", "to / at (with motion: ir a)"],
            ["de", "of / from"],
            ["con / sin", "with / without"],
            ["cerca de / lejos de", "near / far from"],
            ["al lado de", "next to"],
            ["delante de / detrás de", "in front of / behind"],
            ["encima de / debajo de", "on top of / under"],
            ["dentro de / fuera de", "inside / outside"],
            ["entre", "between"],
            ["a la derecha / a la izquierda", "to the right / to the left"],
            ["todo recto / derecho", "straight ahead"],
        ]},
        {"type": "p", "text": (
            "Two fusions you'll see constantly: <es>a + el = al</es> "
            "(<es>Voy al banco</es>) and <es>de + el = del</es> "
            "(<es>cerca del hospital</es>). <es>A la</es> and <es>de la</es> stay as two words."
        )},
        {"type": "pairs", "items": [
            ["El banco está al lado del supermercado.", "The bank is next to the supermarket."],
            ["Vivo cerca de la playa.", "I live near the beach."],
            ["Está a dos cuadras.", "It's two blocks away."],
            ["Gire a la derecha.", "Turn right."],
            ["Venimos de la capital.", "We came from Panama City."],
        ]},
        {"type": "h2", "text": "The personal “a” — when the object is a person"},
        {"type": "p", "text": (
            "English speakers drop this constantly. It is a tiny <es>a</es> before a person "
            "(or a pet you treat like a person). Things do not get it. People will still "
            "understand you without it. Copy it when you can and you will sound less like a textbook in reverse."
        )},
        {"type": "pairs", "items": [
            ["Busco a mi esposa.", "I'm looking for my wife."],
            ["Busco un restaurante.", "I'm looking for a restaurant. (a thing — no a)"],
            ["¿Conoce a un buen dentista?", "Do you know a good dentist?"],
            ["Llamo a María.", "I'm calling María."],
            ["Veo el banco.", "I see the bank. (a thing — no a)"],
            ["Quiero mucho a mi familia.", "I love my family a lot."],
        ]},
    ],
})

add({
    "id": "numbers",
    "kicker": "Chapter 15",
    "title": "Numbers, money, and time",
    "tts_skip_digits": True,
    "intro": (
        "This is the chapter you will use at the caja, the clinic window, and the "
        "taxi door. Panama uses U.S. dollars, so the only conversion is the words."
    ),
    "blocks": [
        {"type": "h2", "text": "Numbers you actually need"},
        {"type": "table", "headers": ["", "", "", ""], "hide_header": True, "emphasis": "all", "rows": [
            ["0 cero", "1 uno", "2 dos", "3 tres"],
            ["4 cuatro", "5 cinco", "6 seis", "7 siete"],
            ["8 ocho", "9 nueve", "10 diez", "11 once"],
            ["12 doce", "13 trece", "14 catorce", "15 quince"],
            ["16 dieciséis", "17 diecisiete", "18 dieciocho", "19 diecinueve"],
            ["20 veinte", "21 veintiuno", "22 veintidós", "30 treinta"],
            ["40 cuarenta", "50 cincuenta", "60 sesenta", "70 setenta"],
            ["80 ochenta", "90 noventa", "100 cien", "101 ciento uno"],
            ["200 doscientos", "500 quinientos", "1,000 mil", "1,000,000 un millón"],
        ]},
        {"type": "ul", "items": [
            "<es>Uno</es> becomes <es>un</es> before a masculine noun: <es>un dólar</es>. <es>Una</es> before feminine: <es>una caja</es>.",
            "200–900 change for gender: <es>doscientos dólares</es>, <es>doscientas cajas</es>.",
            "Years: 2026 is <es>dos mil veintiséis</es>.",
        ]},
        {"type": "h2", "text": "Money"},
        {"type": "pairs", "items": [
            ["¿Cuánto cuesta? / ¿Cuánto es?", "How much does it cost? / How much is it?"],
            ["¿A cómo?", "How much each? (at markets)"],
            ["Está muy caro.", "That's very expensive."],
            ["¿Me puede hacer un precio?", "Can you do a better price?"],
            ["La cuenta, por favor.", "The bill, please."],
            ["¿Tiene cambio? / el vuelto", "Do you have change? / the change you get back"],
            ["en efectivo / con tarjeta", "in cash / by card"],
            ["¿Aceptan tarjeta?", "Do you take cards?"],
        ]},
        {"type": "panama", "title": "Dollars, balboas, and the caja", "text": (
            "Paper money is the U.S. dollar. Local coins are often called "
            "<es>balboas</es>, but they are worth the same as U.S. coins. "
            "<es>La caja</es> is the cashier. <es>La cola</es> is the line. "
            "Tipping is modest — ten percent at sit-down restaurants is a kind default "
            "if service is not already included."
        )},
        {"type": "h2", "text": "What time is it?"},
        {"type": "pairs", "items": [
            ["¿Qué hora es?", "What time is it?"],
            ["Es la una.", "It's one o'clock. (la una is singular)"],
            ["Son las dos.", "It's two o'clock."],
            ["Son las tres y media.", "It's 3:30."],
            ["Son las cuatro y cuarto.", "It's 4:15."],
            ["Son las diez menos diez.", "It's 9:50. (ten to ten)"],
            ["a las nueve de la mañana", "at 9:00 a.m."],
            ["a las siete de la noche", "at 7:00 p.m."],
        ]},
        {"type": "p", "text": (
            "Days: <es>lunes, martes, miércoles, jueves, viernes, sábado, domingo</es>. "
            "They are not capitalized. <es>El lunes</es> means on Monday; "
            "<es>los lunes</es> means on Mondays in general."
        )},
        {"type": "p", "text": (
            "Months: <es>enero, febrero, marzo, abril, mayo, junio, julio, agosto, "
            "septiembre, octubre, noviembre, diciembre</es>. Dates go day first: "
            "<es>el 9 de septiembre</es>."
        )},
    ],
})

add({
    "id": "little-words",
    "kicker": "Chapter 16",
    "title": "Little words that do a lot of work",
    "intro": (
        "These are the glue. If you recognize them, whole sentences stop being a blur."
    ),
    "blocks": [
        {"type": "table", "headers": ["Spanish", "English", "Note"], "rows": [
            ["ya", "already / now", "Also used as “okay, got it.”"],
            ["todavía / aún", "still / yet", "<es>Todavía no</es> = not yet."],
            ["también", "also / too", ""],
            ["tampoco", "neither / not either", "The “no” version of también."],
            ["muy / mucho", "very / a lot", "Muy + adjective: <es>muy caro</es>. Mucho + noun: <es>mucho tráfico</es>."],
            ["más / menos", "more / less", "<es>Más despacio. Menos hielo.</es>"],
            ["ahora / ahorita", "now / in a bit", "Ahorita is famously flexible."],
            ["después / luego", "after / later", ""],
            ["aquí / allí / allá", "here / there / over there", ""],
            ["bien / mal", "well / badly", "¿Todo bien?"],
            ["hoy / mañana / ayer", "today / tomorrow / yesterday", "Mañana is also “morning.”"],
            ["pero / porque / entonces", "but / because / so then", ""],
            ["siempre / nunca", "always / never", "Nunca already includes the no."],
            ["casi", "almost", "<es>Casi nunca</es> = hardly ever."],
        ]},
        {"type": "panama", "title": "Ahorita is a lifestyle", "text": (
            "<es>Ahorita</es> can mean right now, in a few minutes, or later this afternoon, "
            "depending on the smile that comes with it. If you need a real time, ask: "
            "<es>¿A qué hora, más o menos?</es> Around what time?"
        )},
        {"type": "h2", "text": "A few tiny extras you'll hear constantly"},
        {"type": "ul", "items": [
            "<es>-ito / -ita</es> makes things smaller or kinder: <es>momentito, cafecito, abuelita</es>. It is friendly, not baby talk.",
            "<es>lo</es> and <es>la</es> often mean “it” or “him/her,” and they sit in front of the verb: <es>¿Lo vio?</es> Did you see it? <es>La tengo.</es> I have it. If that throws you, just repeat the noun. English speakers trip here more than on verbs — recognition first is enough.",
            "You'll hear <es>se lo</es> a lot: <es>Se lo dije.</es> I told him/her it. You do not have to build this yet. Just know it is not a new verb.",
            "<es>se</es> also shows up on signs: <es>Se vende. Se alquila. Se habla español.</es> For sale. For rent. Spanish spoken here.",
            "<es>Me llamo</es> is technically a reflexive verb. So is <es>Me siento mal</es> (I feel bad). Learn them as phrases.",
        ]},
    ],
})

add({
    "id": "panama",
    "kicker": "Chapter 17",
    "title": "Panama Spanish, the local layer",
    "intro": (
        "You do not need slang to buy papayas. But a few local habits will make the "
        "country sound less like your textbook and more like the taxi."
    ),
    "blocks": [
        {"type": "table", "headers": ["You'll hear", "What they mean"], "rows": [
            ["la capital", "Panama City"],
            ["el interior", "the rest of the country, outside the city"],
            ["chévere", "great, cool, nice"],
            ["¿Qué xopá?", "What's up? (very Panama; you can just smile back)"],
            ["pelao / pelaíta", "kid / young person"],
            ["la plata", "money"],
            ["un chance", "a ride (¿Me da un chance?)"],
            ["la bomba", "the gas station (yes, also “bomb” — context will save you)"],
            ["el abanico", "the fan"],
            ["la chitra", "no-see-ums, the tiny biting bugs"],
            ["diablo rojo", "the old painted buses"],
            ["el Metro / Metrobus", "Panama City's subway and bus system"],
            ["farmacia de turno", "the pharmacy on duty that night"],
            ["se fue la luz / el agua", "the power / water went out"],
            ["¡Juega viva!", "stay sharp / watch out (friendly warning)"],
        ]},
        {"type": "ul", "items": [
            "There is no <es>vos</es> here (that's more Costa Rica, Nicaragua, Argentina). Stick with <es>tú</es> and <es>usted</es>.",
            "There is no <es>vosotros</es>. Groups are <es>ustedes</es>.",
            "<es>Guagua</es> is not the Panama word for bus. Say <es>bus</es>.",
            "English sneaks in: <es>el parking, el mall, el email, okay</es>. You are allowed to mix a little.",
            "People may answer your careful Spanish with English. That is kindness, not a correction.",
        ]},
        {"type": "h2", "text": "A note you can leave for the building manager"},
        {"type": "note", "text": (
            "Estimado señor / Estimada señora:\n\n"
            "Soy su vecino/a del apartamento ____. Se fue el agua esta mañana "
            "(or: El aire no funciona / Hay una gotera en el techo). "
            "¿Puede ayudarnos, por favor?\n\n"
            "Muchas gracias,\n"
            "____________________"
        )},
    ],
})

add({
    "id": "phrasebook",
    "kicker": "Chapter 18",
    "title": "Phrasebook for a regular week",
    "intro": (
        "Keep this chapter on your phone. Read the Spanish out loud once before you "
        "walk in. Close enough is plenty."
    ),
    "blocks": [
        {"type": "h2", "text": "Greetings and good manners"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["Buenos días. / Buenas tardes. / Buenas noches.", "Good morning. / Good afternoon. / Good evening."],
            ["¿Cómo está usted? — Bien, gracias. ¿Y usted?", "How are you? — Fine, thanks. And you?"],
            ["Mucho gusto. / El gusto es mío.", "Nice to meet you. / The pleasure is mine."],
            ["¿Cómo se llama? — Me llamo…", "What's your name? — My name is…"],
            ["Con permiso. / Perdón.", "Excuse me (passing through). / Sorry / pardon me."],
            ["Por favor. / Gracias. / De nada.", "Please. / Thank you. / You're welcome."],
            ["Hasta luego. / Nos vemos. / Que le vaya bien.", "See you later. / See you. / Take care."],
        ]},
        {"type": "h2", "text": "When the Spanish is too fast"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["No hablo español muy bien.", "I don't speak Spanish very well."],
            ["¿Habla inglés?", "Do you speak English?"],
            ["Más despacio, por favor.", "More slowly, please."],
            ["¿Puede repetir?", "Can you repeat that?"],
            ["¿Cómo se dice … en español?", "How do you say … in Spanish?"],
            ["¿Qué significa esto?", "What does this mean?"],
            ["¿Me lo puede escribir?", "Can you write it down for me?"],
            ["Un momento, por favor. Voy a usar el traductor.", "One moment, please. I'm going to use the translator."],
        ]},
        {"type": "h2", "text": "At the clinic"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["Tengo una cita a las diez.", "I have a ten o'clock appointment."],
            ["Me duele aquí. / Me duele la cabeza.", "It hurts here. / I have a headache."],
            ["Me duele el estómago / la espalda / la rodilla.", "My stomach / back / knee hurts."],
            ["Tengo mareos / fiebre / tos / náuseas.", "I have dizziness / a fever / a cough / nausea."],
            ["Me siento mareado/a. / Me siento mal.", "I feel dizzy. / I feel unwell."],
            ["Soy alérgico/a a la penicilina.", "I'm allergic to penicillin."],
            ["Tomo estos medicamentos. (show the list)", "I take these medications."],
            ["Tengo presión alta / diabetes.", "I have high blood pressure / diabetes."],
            ["Soy jubilado/a.", "I'm retired."],
            ["¿Es grave? / ¿Qué tengo?", "Is it serious? / What do I have?"],
            ["¿Cuándo vuelvo?", "When do I come back?"],
        ]},
        {"type": "h2", "text": "At the pharmacy"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["¿Tiene algo para el dolor / el resfriado / la alergia?", "Do you have something for pain / a cold / allergies?"],
            ["Necesito esto. (show paper or bottle)", "I need this."],
            ["¿Es con receta?", "Is it by prescription?"],
            ["Una caja, por favor.", "One box, please."],
            ["¿Cómo se toma?", "How do you take it?"],
            ["¿Cada cuántas horas?", "Every how many hours?"],
            ["Con comida / con el estómago vacío.", "With food / on an empty stomach."],
        ]},
        {"type": "h2", "text": "Eating out"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["Una mesa para dos, por favor.", "A table for two, please."],
            ["El menú, por favor.", "The menu, please."],
            ["¿Qué recomienda?", "What do you recommend?"],
            ["Agua sin gas / con gas. Sin hielo, por favor.", "Still / sparkling water. No ice, please."],
            ["No picante, por favor.", "Not spicy, please."],
            ["Está delicioso.", "It's delicious."],
            ["Para llevar.", "To go."],
            ["La cuenta, por favor.", "The bill, please."],
            ["¿Propina incluida? / ¿Está incluida la propina?", "Is the tip included?"],
        ]},
        {"type": "h2", "text": "At home with a plumber, electrician, or gardener"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["Se fue la luz / el agua / el internet.", "The power / water / internet went out."],
            ["El aire no enfría.", "The air conditioning isn't cooling."],
            ["Hay una gotera en el techo.", "There's a leak in the roof."],
            ["El inodoro no funciona.", "The toilet doesn't work."],
            ["¿Puede arreglarlo?", "Can you fix it?"],
            ["¿Cuánto cobra?", "How much do you charge?"],
            ["¿Puede venir hoy / mañana?", "Can you come today / tomorrow?"],
            ["¿A qué hora?", "At what time?"],
        ]},
        {"type": "h2", "text": "Getting around"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["¿Está libre?", "Are you free? (taxi)"],
            ["Al Hospital Paitilla, por favor.", "To Paitilla Hospital, please."],
            ["¿Cuánto es hasta…?", "How much is it to…?"],
            ["Aquí está bien. Gracias.", "Here is fine. Thank you."],
            ["¿Dónde está la parada del bus / del Metro?", "Where is the bus / Metro stop?"],
            ["Un taxi, por favor.", "A taxi, please."],
        ]},
        {"type": "h2", "text": "Neighbors and small talk"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["Somos vecinos. Vivimos en…", "We're neighbors. We live in…"],
            ["¿Me puede recomendar un buen dentista / restaurante / plomero?", "Can you recommend a good dentist / restaurant / plumber?"],
            ["Está muy rico el café.", "This coffee is really good."],
            ["¡Qué calor!", "So hot!"],
            ["Que descanse.", "Rest well. (a warm evening goodbye)"],
        ]},
        {"type": "h2", "text": "Emergencies"},
        {"type": "phrases", "columns": ["Spanish", "English"], "rows": [
            ["¡Ayuda, por favor!", "Help, please!"],
            ["Llame a una ambulancia.", "Call an ambulance."],
            ["Necesito un médico ahora.", "I need a doctor now."],
            ["Me siento muy mal.", "I feel very ill."],
            ["Hubo un accidente.", "There was an accident."],
            ["Policía, por favor.", "Police, please."],
        ]},
        {"type": "tip", "title": "911 works in Panama", "text": (
            "You can dial 911 for police, fire, and ambulance. If you can, also tell "
            "someone nearby: <es>Llame al nueve once, por favor.</es>"
        )},
    ],
})

add({
    "id": "cheatsheets",
    "kicker": "Keep this page",
    "title": "Cheat sheets",
    "newpage": True,
    "compact": True,
    "intro": "The whole booklet in a few little boxes. Take a photo of this page.",
    "blocks": [
        {"type": "h2", "text": "Ser vs. estar vs. hay"},
        {"type": "table", "headers": ["Use", "When", "Example"], "audio_cols": [0, 2], "rows": [
            ["ser", "who / what / origin / time / job", "Soy jubilado. Es martes. Somos de Ohio."],
            ["estar", "where / how you feel / open-closed", "Estoy en David. Está cerrado. Estoy cansado."],
            ["hay", "there is / there are", "¿Hay un cajero cerca?"],
        ]},
        {"type": "h2", "text": "Two pasts"},
        {"type": "table", "headers": ["If English can say…", "Use", "Example"], "audio_cols": [2], "rows": [
            ["I did it (and it finished)", "snapshot", "Ayer fui al médico. Comí pescado."],
            ["I used to / I was -ing", "background", "Cuando vivía en Florida… Hacía calor."],
        ]},
        {"type": "h2", "text": "The sentence machines"},
        {"type": "table", "headers": ["Start with", "Add", "You get"], "audio_cols": [0, 2], "rows": [
            ["Quiero…", "a noun or a verb", "Quiero agua. Quiero pagar."],
            ["Necesito…", "a noun or a verb", "Necesito ayuda. Necesito descansar."],
            ["¿Puede…?", "a verb", "¿Puede repetir? ¿Puede ayudarme?"],
            ["Tengo que…", "a verb", "Tengo que ir al banco."],
            ["Voy a…", "a verb", "Voy a llamar mañana."],
            ["Me gusta / Me gustan…", "the thing you like", "Me gusta el café. Me gustan las islas."],
            ["¿Dónde está…?", "a place or thing", "¿Dónde está la caja?"],
            ["¿Cuánto cuesta…?", "a thing", "¿Cuánto cuesta esto?"],
            ["Busco a…", "a person", "Busco a María. (things skip the a)"],
        ]},
        {"type": "p", "text": (
            "Tricky gender, with the article: <es>el día, el mapa, el problema, el agua, "
            "la mano, la foto</es>."
        )},
    ],
})

add({
    "id": "pocket",
    "kicker": "Pocket page",
    "title": "If you only carry one page",
    "newpage": True,
    "compact": True,
    "intro": (
        "Fold this. Keep it in your wallet. Point at a line if the words will not come."
    ),
    "blocks": [
        {"type": "table", "headers": ["Spanish", "English", "Spanish", "English"],
         "audio_cols": [0, 2], "rows": [
            ["Más despacio, por favor.", "A little slower, please.",
             "No hablo español muy bien.", "I don't speak Spanish well."],
            ["¿Me puede ayudar?", "Can you help me?",
             "¿Habla inglés?", "Do you speak English?"],
            ["¿Cuánto cuesta?", "How much is it?",
             "Quiero esto, por favor.", "I want this, please."],
            ["¿Dónde está el baño?", "Where is the bathroom?",
             "Tengo una cita.", "I have an appointment."],
            ["Me duele aquí.", "It hurts here.",
             "Se fue la luz / el agua.", "The power / water went out."],
            ["¿Puede repetir?", "Can you repeat that?",
             "Gracias. / Por favor.", "Thank you. / Please."],
            ["Que le vaya bien.", "Take care.",
             "Llame a una ambulancia.", "Call an ambulance."],
        ]},
        {"type": "tip", "title": "Ánimo. You've got this.", "text": (
            "911 works in Panama. Say <es>Llame al nueve once, por favor.</es> "
            "Use <es>usted</es> with people you don't know well. Close enough is plenty."
        )},
    ],
})
