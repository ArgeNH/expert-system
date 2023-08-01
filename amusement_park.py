from experta import Fact, Rule, KnowledgeEngine, Field, DefFacts, AS, MATCH, P


class Visitor(Fact):
    height = Field(float, mandatory=True)
    age = Field(int, mandatory=True)
    ticket = Field(str, mandatory=True)  # 'General' o 'VIP'
    heart_condition = Field(bool, mandatory=True)
    pregnant = Field(bool, mandatory=True)


class Attraction(Fact):
    name = Field(str, mandatory=True)
    min_height = Field(float, mandatory=True)
    max_age = Field(int, mandatory=True)
    ticket_required = Field(str, mandatory=True)  # 'General' o 'VIP'
    # Si es una atracción de alta velocidad
    is_high_speed = Field(bool, mandatory=True)


class Park(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        height = float(input("Por favor, introduce tu altura en metros: "))
        age = int(input("Por favor, introduce tu edad: "))
        ticket = input("¿Qué tipo de boleto tienes? (General/VIP): ")
        heart_condition = input(
            "¿Tienes alguna condición de corazón? (si/no): ") == 'si'
        pregnant = input("¿Estás embarazada? (si/no): ") == 'si'
        yield Visitor(height=height, age=age, ticket=ticket, heart_condition=heart_condition, pregnant=pregnant)

        # Agregar hechos para cada atracción
        yield Attraction(
            name='Montaña rusa',
            min_height=1.5,
            max_age=60,
            ticket_required='General',
            is_high_speed=True
        )
        yield Attraction(
            name='Carrusel',
            min_height=0.0,
            max_age=100,
            ticket_required='General',
            is_high_speed=False
        )
        yield Attraction(
            name='Casa del terror',
            min_height=1.2,
            max_age=80,
            ticket_required='VIP',
            is_high_speed=False
        )
        yield Attraction(
            name='Tobogán de agua',
            min_height=1.3,
            max_age=55,
            ticket_required='VIP',
            is_high_speed=True
        )
        yield Attraction(
            name='La rueda de la fortuna',
            min_height=1.0,
            max_age=80,
            ticket_required='General',
            is_high_speed=False
        )

    @Rule(Visitor(height=MATCH.h, age=MATCH.a, ticket=MATCH.t, heart_condition=MATCH.hc, pregnant=MATCH.p),
          Attraction(name=MATCH.n, min_height=MATCH.mh & P(lambda mh: mh > 1.5), max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_1(self, n):
        print(f"No puedes subirte a {n} debido a tu altura.")

    @Rule(Visitor(height=MATCH.h, age=MATCH.a, ticket=MATCH.t, heart_condition=True, pregnant=MATCH.p),
          Attraction(name=MATCH.n, min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=True))
    def rule_2(self, n):
        print(f"No puedes subirte a {n} debido a tu condición de corazón.")

    @Rule(Visitor(height=MATCH.h, age=MATCH.a, ticket=MATCH.t, heart_condition=MATCH.hc, pregnant=True),
          Attraction(name=MATCH.n, min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=True))
    def rule_3(self, n):
        print(f"No puedes subirte a {n} debido a tu estado de embarazo.")

    @Rule(Visitor(height=MATCH.h, age=MATCH.a, ticket=MATCH.t & P(lambda t: t != 'VIP'), heart_condition=MATCH.hc, pregnant=MATCH.p),
          Attraction(name=MATCH.n, min_height=MATCH.mh, max_age=MATCH.ma, ticket_required='VIP', is_high_speed=MATCH.hs))
    def rule_4(self, n):
        print(f"No puedes subirte a {n} porque necesitas un boleto VIP.")

    @Rule(Visitor(height=MATCH.h & P(lambda h: h >= 1.5), age=MATCH.a & P(lambda a: a <= 60), ticket='General', heart_condition=False, pregnant=False),
          Attraction(name='Montaña rusa', min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_5(self):
        print("¡Puedes subirte a la Montaña rusa!")

    @Rule(Visitor(height=MATCH.h & P(lambda h: h >= 0.0), age=MATCH.a & P(lambda a: a <= 100), ticket='General', heart_condition=False, pregnant=False),
          Attraction(name='Carrusel', min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_6(self):
        print("¡Puedes subirte al Carrusel!")

    @Rule(Visitor(height=MATCH.h & P(lambda h: h >= 1.2), age=MATCH.a & P(lambda a: a <= 80), ticket='VIP', heart_condition=MATCH.hc, pregnant=MATCH.p),
          Attraction(name='Casa del terror', min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_7(self):
        print("¡Puedes entrar a la Casa del terror!")

    @Rule(Visitor(height=MATCH.h & P(lambda h: h >= 1.3), age=MATCH.a & P(lambda a: a <= 55), ticket='VIP', heart_condition=False, pregnant=False),
          Attraction(name='Tobogán de agua', min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_8(self):
        print("¡Puedes subirte al Tobogán de agua!")

    @Rule(Visitor(height=MATCH.h & P(lambda h: h >= 1.0), age=MATCH.a & P(lambda a: a <= 80), ticket='General', heart_condition=MATCH.hc, pregnant=MATCH.p),
          Attraction(name='La rueda de la fortuna', min_height=MATCH.mh, max_age=MATCH.ma, ticket_required=MATCH.tr, is_high_speed=MATCH.hs))
    def rule_9(self):
        print("¡Puedes subirte a la Rueda de la fortuna!")


engine = Park()
engine.reset()
engine.run()
