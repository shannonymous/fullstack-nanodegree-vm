from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SportCategory, Base, SportItem, User

engine = create_engine("sqlite:///sportswithusers.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won"t be persisted into the database until you call
# session.commit(). If you"re not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()



category1 = SportCategory(name = "Football", user_id=1)
session.add(category1)
session.commit()

<<<<<<< HEAD
item1 = SportItem(name="Gloves", description="No matter if you're a skill player or a lineman in the trenches, football gloves help players gain an edge on the field. Receivers, running backs and defensive backs depend on football gloves to grip the ball, while linemen benefit from the added warmth and protection gloves provide.", sport=category1, user_id=1)
||||||| merged common ancestors
item1 = SportItem(name="Gloves", description="No matter if you're a skill player or a lineman in the trenches, football gloves help players gain an edge on the field. Receivers, running backs and defensive backs depend on football gloves to grip the ball, while linemen benefit from the added warmth and protection gloves provide.", sport=category1)
=======
item1 = SportItem(name="Gloves", description="No matter if you're a skill player or a lineman in the trenches, football gloves help players gain an edge on the field. Receivers, running backs and defensive backs depend on football gloves to grip the ball, while linemen benefit from the added warmth and protection gloves provide.", sport=category1, , user_id=1)
>>>>>>> c7eef9bd13001abd40acf946c9f2a380af469d1e

session.add(item1)
session.commit()

item2 = SportItem(name="Football Cleats", description="Find the latest football boots from Nike, adidas, Puma, Umbro & many more", sport=category1, user_id=1)

session.add(item2)
session.commit()

item3 = SportItem(name="Football", description="A football is a ball inflated with air that is used to play one of the various sports known as football. In these games, with some exceptions, goals or points are scored only when the ball enters one of two designated goal-scoring areas; football games involve the two teams each trying to move the ball in opposite directions along the field of play.", sport=category1, user_id=1)

session.add(item3)
session.commit()



category2 = SportCategory(name = "Basketball", user_id=1)
session.add(category2)
session.commit()


item1 = SportItem(name="Shoes", description="One needs specialized shoes when playing basketball. It should be able to give better support to the ankle as compared to running shoes. The basketball shoes should be high-tipped shoes and provide extra comfort during a game. These shoes are specially designed to maintain high traction on the basketball court.", sport=category2, user_id=1)

session.add(item1)
session.commit()

item2 = SportItem(name="Hoop", description="The hoop or basket is a horizontal metallic rim, circular in shape. This rim is attached to a net and helps one score a point. The rim is mounted about 4 feet inside the baseline and 10 feet above the court.", sport=category2, user_id=1)

session.add(item2)
session.commit()

item3 = SportItem(name="Shot Clock", description="The offense is allowed a maximum of 24 seconds to have a ball in hand before shooting. These 24 seconds are counted on the shot clock. If the offense fails to shoot a ball that hits the rim, they will lose the possession of the ball to the other team.", sport=category2, user_id=1)

session.add(item3)
session.commit()

item4 = SportItem(name="The Ball", description="The most important thing for training is the ball. There are certain guidelines which one needs to follow when buying a basketball. For practicing, one can play with a rubber ball. For professional competitions, one needs to use an inflated ball made of leather. Official size of a basketball is 29.5 to 30 inches in circumference for men's game and 28.5 inches in circumference for women's game. It should weigh 18 to 22 ounces. When bounced off 6 feet from the floor, a well inflated ball should bounce 49 to 54 inches in height.", sport=category2, user_id=1)

session.add(item4)
session.commit()

item5 = SportItem(name="Court", description="The court is usually made of wooden floorboard. The court size is about 28m x 17m according to the International standards. The National Basketball Association (NBA) regulation states the floor dimension as 29m x 15m. The standard court is rectangular in shape and has baskets placed on opposite ends.", sport=category2, user_id=1)

session.add(item5)
session.commit()

category3 = SportCategory(name = "Ultimate Frisbee", user_id=1)
session.add(category3)
session.commit()


item1 = SportItem(name="Frisbee", description="A frisbee is a gliding toy or sporting item that is generally plastic and roughly 8 to 10 inches (20 to 25 cm) in diameter with a pronounced lip.", sport=category3, user_id=1)

session.add(item1)
session.commit()

item2 = SportItem(name="Ultimate Gloves", description="Ultimate Frisbee gloves offer the perfect amount of traction in both wet and dry conditions. Even the wettest disc is no match for its superior leather palms", sport=category3, user_id=1)

session.add(item2)
session.commit()

item3 = SportItem(name="Scorekeeping Watch", description="A digital watch that is lightweight, durable, and has four functions. This handy little watch is capable of keeping score.", sport=category3, user_id=1)

session.add(item3)
session.commit()


item4 = SportItem(name="Compression Arm Sleeve", description="These are otherwise known as bidding sleeves. Ultimate players like to wear these on their throwing arm for two reasons: The sleeve absorbs sweat making it easier to throw and it resists scrapes, burns, and cuts on the elbow from bidding/falling.", sport=category3, user_id=1)

session.add(item4)
session.commit()

category4 = SportCategory(name = "Baseball", user_id=1)
session.add(category4)
session.commit()

item1 = SportItem(name="Bat", description="A rounded, solid wooden or hollow aluminum bat. Wooden bats are traditionally made from ash wood, though maple and bamboo is also sometimes used. Aluminum bats are not permitted in professional leagues, but are frequently used in amateur leagues. Composite bats are also available, essentially wooden bats with a metal rod inside. Bamboo bats are also becoming popular.", sport=category4, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Base", description="One of four corners of the infield which must be touched by a runner in order to score a run; more specifically, they are canvas bags (at first, second, and third base) and a rubber plate (at home).", sport=category4, user_id=1)
session.add(item2)
session.commit()

item3 = SportItem(name="Glove", description="Leather gloves worn by players in the field. Long fingers and a webbed 'KKK' between the thumb and first finger allows the fielder to catch the ball more easily.", sport=category4, user_id=1)
session.add(item3)
session.commit()

category5 = SportCategory(name = "Snowboarding", user_id=1)
session.add(category5)
session.commit()

item1 = SportItem(name="Ski Gear", description="Snowboarders must wear hot and good quality clothes against the cold temperature.", sport=category5, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Ski Goggles", description="To protect their eyes from reflection of the sun on the snow, against the snow and the wind that can be very hurtful. It is essential to have a good view during the ride.", sport=category5, user_id=1)
session.add(item2)
session.commit()

item3 = SportItem(name="Bindings", description="To provide snowboarders solidity and stability. The security attach have to be firmly tied on the binding and clip on one of your boots adapted to this sport.", sport=category5, user_id=1)
session.add(item3)
session.commit()

category6 = SportCategory(name = "Rockclimbing", user_id=1)
session.add(category6)
session.commit()

item1 = SportItem(name="Carabiners", description="Carabiners are metal loops with spring-loaded gates (openings), used as connectors. Once made primarily from steel, almost all carabiners for recreational climbing are now made from a light weight aluminum alloy. Steel carabiners are much heavier, but harder wearing, and therefore are often used by instructors when working with groups.", sport=category6, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Harness", description="A harness is a system used for connecting the rope to the climber. There are two loops at the front of the harness where the climber ties into the rope at the working end using a figure-eight knot]]. Most harnesses used in climbing are preconstructed and are worn around the pelvis and hips, although other types are used occasionally.", sport=category6, user_id=1)
session.add(item2)
session.commit()

item3 = SportItem(name="Belay", description="Belay devices are mechanical friction brake devices used to control a rope when belaying. Their main purpose is to allow the rope to be locked off with minimal effort to arrest a climber's fall. Multiple kinds of belay devices exist, some of which may additionally be used as descenders for controlled descent on a rope, as in abseiling or rappelling.", sport=category6, user_id=1)
session.add(item3)
session.commit()


category7 = SportCategory(name = "Hockey", user_id=1)
session.add(category7)
session.commit()

item1 = SportItem(name="Shin Guards", description="When you play field hockey, your shins take the most beating from balls and sticks. It is thus important for you to protect your shins from getting bruised.", sport=category7, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Hockey Stick", description="The hockey stick that is used is a J shape and made out of wood, glass and fibre. The stick has a curve hook at the end.", sport=category7, user_id=1)
session.add(item2)
session.commit()

item3 = SportItem(name="Mouth Guard", description="Investing in a mouth guard is a good idea because you wouldn't want to burn a hole in your wallet, paying for your dental treatment should a ball hit you in the face. ", sport=category7, user_id=1)
session.add(item3)
session.commit()

item4 = SportItem(name="Socks and Rash Guards", description="Socks are pretty common sense. If you refuse to wear socks then, brace yourself for the blisters. Rash guards on the other hand, are optional. They go under your shin guards and protect your shin from getting constantly rubbed against the shin guards.", sport=category7, user_id=1)
session.add(item4)
session.commit()

item5 = SportItem(name="Electrical Tape", description="Electrical tape is really useful and if you tape them to the bottom of your stick, it protects your stick from dents and wear and tear! If you're a beginner, taping the bottom of your stick would also aid in stopping the ball.", sport=category7, user_id=1)
session.add(item5)
session.commit()

item6 = SportItem(name="Grip", description="If you're going to be using your hockey stick regularly, then you would realise that the grip at the top wears easily. Buying and replacing grips would be common once you become a hockey player.", sport=category7, user_id=1)
session.add(item6)
session.commit()

category8 = SportCategory(name = "Skating", user_id=1)
session.add(category8)
session.commit()

item1 = SportItem(name="Boots", description="Ice skating boots are constructed from stiff leather to provide support to the ankle and foot. The most important thing to consider when buying ice skating boots is the fit. The boot should be snug and your foot should not be able to move around much. The boots will become more comfortable once they are broken in, but if a boot pinches or causes numbness, it is not the right size. Many boots sold in sports equipment outlets come with the blades already attached, which is fine for a beginner or recreational skater. But competitive skaters should buy their boots and then have the blades fitted and attached.", sport=category8, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Blades", description="Ice skating blades are not completely flat from one tip to the other. Instead, they have a small curve referred to as the rocker. The width of the blade is not completely flat either, it is concave, which creates two sharp edges. In turn, there are four points on the blade that can be used in executing various moves, spins and jumps. The front of the blade is serrated and referred to as the toe pick. The length of the blade and the size of the toe pick will vary depending on specialized style and skill level. It is important to regularly sharpen your skate blades and to protect them when you're not on the ice.", sport=category8, user_id=1)
session.add(item2)
session.commit()


category9 = SportCategory(name = "Fencing", user_id=1)
session.add(category9)
session.commit()

item1 = SportItem(name="Foil", description="The foil is a light and easy to bend weapon, first made in mid 17th century as a weapon for practice. 'Hits' can only be scored by hitting the target area with the point of the sword. The target area is the torso.", sport=category9, user_id=1)
session.add(item1)
session.commit()

item2 = SportItem(name="Epee", description="The epee is the heaviest of the three weapons. To score a hit, the push-button on the end of the weapon must remain fully down for 2-10 milliseconds, and must arrive (hit) with a force of at least 7.35 newtons. The target area for Epee is the entire body. This includes the feet and the head.", sport=category9, user_id=1)
session.add(item2)
session.commit()

<<<<<<< HEAD
item3 = SportItem(name="Sabre", description="The sabre is the 'cutting' weapon, with a curved guard (to protect the hand) and a triangular blade. However, in modern electric scoring, a touch with any part of the sabre, (point, flat or edge, as long as it is on target) will count as a hit. The target area in sabre is everything from the waist up, except for the hands.", sport=category9, user_id=1)
||||||| merged common ancestors
item3 = SportItem(name="Foil", description="The sabre is the 'cutting' weapon, with a curved guard (to protect the hand) and a triangular blade. However, in modern electric scoring, a touch with any part of the sabre, (point, flat or edge, as long as it is on target) will count as a hit. The target area in sabre is everything from the waist up, except for the hands.", sport=category9)
=======
item3 = SportItem(name="Foil", description="The sabre is the 'cutting' weapon, with a curved guard (to protect the hand) and a triangular blade. However, in modern electric scoring, a touch with any part of the sabre, (point, flat or edge, as long as it is on target) will count as a hit. The target area in sabre is everything from the waist up, except for the hands.", sport=category9, user_id=1)
>>>>>>> c7eef9bd13001abd40acf946c9f2a380af469d1e
session.add(item3)
session.commit()


print "added database items!"
