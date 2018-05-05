import pygame
import sys
from pygame.locals import*
import random
from classe_tiles import*
import ctypes
from Ship_Shooter import*


pygame.init()  #Démarrage de pygame
pygame.mixer.init()
screen = pygame.display.set_mode((LARGEUR,HAUTEUR), RESIZABLE) #On définit les dimensions de la page
pygame.display.set_caption("Accueil")


#Chargement et collage du fond
fond = pygame.image.load("fond.jpg").convert() #dimension: 672 sur 672
pac_fond = pygame.image.load("background1.png").convert()
screen.blit(fond, (0,0))

#Chargement et collage de la fenêtre qui renvoie sur le pacman ( dimension: 224 sur 75)
persoP = pygame.image.load("Pacman.png").convert_alpha()  
persoP_x = 224  
persoP_y =329
persoP_x2 =448
persoP_y2 =404

screen.blit(persoP, (persoP_x, persoP_y))
#Chargement et collage de la fenêtre qui renvoie sur le shooter ( dimension 224 sur 75)
persoS = pygame.image.load("Shooter.png").convert_alpha()
persoS_x =224
persoS_y =448
persoS_x2 =448
persoS_y2 =523
screen.blit(persoS, (persoS_x, persoS_y))


#Chargement de la fenêtre "Recommencer" et "Quitter"
persoR = pygame.image.load("Restart.png").convert_alpha()
persoR_x =214
persoR_y =240
persoR_x2 =458
persoR_y2 =288

persoQ = pygame.image.load("Quitter.png").convert_alpha()
persoQ_x =214
persoQ_y =344
persoQ_x2 =458
persoQ_y2 =392

#Rafraîchissement de l'écran
pygame.display.flip()

#Définition des valeurs des boucles
acc_continuer = 1
pac_continuer = 0
ship_continuer = 0
restart = 0
pacpac=0
shipship=0
infinite = 1
niveau = Niveau('n1.txt')
niveau.generer()
niveau.afficher(screen)

while infinite:   #Boucle infinie qui permet au jeu de tourner sans s'arrêter

	while acc_continuer:
		for event in pygame.event.get():	#Attente des événements
			if event.type == QUIT:
				infinite = 0
			if event.type == KEYDOWN :  #Attente de la pression d'une touche
				if event.key == K_ESCAPE :  #Si on appuit sur échap, le jeu quitte.
					infinite = 0
			if event.type == MOUSEBUTTONDOWN:    #Si on clique gauche
				if event.button == 1:	
					if event.pos[0]>= persoP_x and event.pos[0]<= persoP_x2 and event.pos[1]>= persoP_y and event.pos[1]<= persoP_y2 :   #si on clique sur la fenêtre du pacman
																	pac_continuer = 1  #Ouvrir Pacman
																	acc_continuer = 0
					if event.pos[0]>= persoS_x and event.pos[0]<= persoS_x2 and event.pos[1]>= persoS_y and event.pos[1]<= persoS_y2 :   
																	ship_continuer = 1 #Ouvrir Shooter
																	acc_continuer = 0
					
			if event.type == MOUSEMOTION: #Segment qui permet de changer l'image si la souris passe dessus		
					if event.pos[0]>= persoP_x and event.pos[0]<= persoP_x2 and event.pos[1]>= persoP_y and event.pos[1]<= persoP_y2 : #si souris passe sur fenêtre pacman
																	persoP = pygame.image.load("Pacman2.png").convert_alpha()
					else :
						persoP = pygame.image.load("Pacman.png").convert_alpha()
					if event.pos[0]>= persoS_x and event.pos[0]<= persoS_x2 and event.pos[1]>= persoS_y and event.pos[1]<= persoS_y2 :
																	persoS = pygame.image.load("Shooter2.png").convert_alpha()		
					else :

						persoS = pygame.image.load("Shooter.png").convert_alpha()
		#Re-collage
		screen.blit(fond, (0,0))	
		screen.blit(persoP, (persoP_x, persoP_y))
		screen.blit(persoS, (persoS_x, persoS_y))
		
		#Rafraichissement
		pygame.display.flip()


	if pac_continuer: #Si le pac-man est ouvert, on réinitialise toutes les valeurs.
		pacpac=1
		shipship=0
		all_sprites.add(pac,ghost1,ghost2,ghost3,ghost4)#On rajoute les sprites aux groupes, s'ils ont disparus au cours d'une partie
		ghosts.add(ghost1,ghost2,ghost3,ghost4)
		(pac.rect.centerx,pac.rect.centery) = pac_pos #Valeurs du pac-man
		Pac.left,Pac.right,Pac.down,Pac.up = 0,1,0,0
		Pac.bonus ,Pac.anim ,Pac.calm ,Pac.temps_now,Pac.orientation = 0,1,0,0,0
		pac.up_delay,pac.down_delay,pac.left_delay,pac.right_delay = 0,0,0,1

		(ghost1.rect.centerx,ghost1.rect.centery) = ghost1_pos #Valeurs du fantome 1
		Ghost1.left=0
		Ghost1.right=0
		Ghost1.up=1
		Ghost1.down=0
		ghost1.posx = 0
		ghost1.posy = 0

		ghost1.priority = 0

		(ghost2.rect.centerx,ghost2.rect.centery) = ghost2_pos #Valeurs du fantome 2, etc...
		Ghost2.left=0
		Ghost2.right=0
		Ghost2.up=0
		Ghost2.down=1
		ghost2.posx = 0
		ghost2.posy = 0

		ghost2.priority = 0

		(ghost3.rect.centerx,ghost3.rect.centery) = ghost3_pos
		Ghost3.left=0
		Ghost3.right=1
		Ghost3.up=0
		Ghost3.down=0
		ghost3.posx = 0
		ghost3.posy = 0

		ghost3.priority = 0

		(ghost4.rect.centerx,ghost4.rect.centery) = ghost4_pos
		Ghost4.left=1
		Ghost4.right=0
		Ghost4.up=0
		Ghost4.down=0
		ghost4.posx = 0
		ghost4.posy = 0

		ghost4.priority = 0

		
	while pac_continuer == 1: #Boucle du jeu Pac-Man
		clock.tick(FPS)
		temps_update = pygame.time.get_ticks() #Permet de garder la valeur du temps passé en millisecondes

		
		if not pac.alive(): #Game Over si le sprite du pac-man disparait
			pac_continuer = 0
			restart = 1
			
		if Pac.calm == 1 and temps_update - Pac.temps_now > 10000: #Les fantomes s'énervent 10000ms, soit 10 secondes
			Pac.calm = 0

			
		for event in pygame.event.get():   #Attente d'évènements
			if event.type == pygame.QUIT: #Quitte le jeu si la fenêtre est fermée
				acc_continuer = 0
				continuer = 0

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: #Retour à l'accueil si "échap"
					acc_continuer=1
					pac_continuer=0

			
		
		#Rafraichissement des sprites, puis affichages du fond, des sprites et des fantomes.
		screen.blit(pac_fond, (0,0))
		all_sprites.update()
		ghosts.update()
		all_sprites.draw(screen)
		ghosts.draw(screen)
		s.draw(screen, (index%16)+Pac.orientation*4, pac.rect.centerx, pac.rect.centery, CENTER_HANDLE)
		index += 1
		pygame.display.flip()

		
	if ship_continuer: #Les valeurs sont réinitialisées si le Shooter est lancé.
		pacpac=0
		shipship=1
		pygame.mixer.music.load('Sounds/F-777 - Space Battle.wav') #Recommence la musique
		pygame.mixer.music.set_volume(0.2)
		pygame.mixer.music.play(loops=-1)
		ship_sprite.add(ship) #Si le sprites du vaisseau n'existe pas, il réapparait
		ship.life = 100 #Réinitialise sa vie et ses coordonnées
		ship.rect.centerx= LARGEUR/2
		ship.rect.bottom= HAUTEUR*0.9
		sec = 0
		meteors.empty() #Suppression des anciennes météores et des nouvelles météores apparaissent
		for i in range (15):
			new_meteor()
  

	while ship_continuer:
		clock.tick(FPS)
		#Décompte du temps, et on marque les secondes
		temps_mtn = pygame.time.get_ticks()
		if temps_mtn-temps >= 993:
			print(sec)
			sec += 1
			temps=temps_mtn
		
		for event in pygame.event.get(): #Permet encore de quitter le jeu. Et arrête la musique si le quitte
			if event.type == pygame.QUIT:
				acc_continuer = 1
				ship_continuer = 0
				pygame.mixer.music.stop()
		
		if event.type == KEYDOWN :
				if event.key == K_ESCAPE:
					ship_continuer = 0
					pygame.mixer.music.stop()
					acc_continuer = 1			
						
						

		
		
		hits = pygame.sprite.groupcollide(meteors, bullets, True, True) #Si les météores touchent les bullets, les deux disparaissent et un nouveau météore apparait.
		for hit in hits:
			explosion1_sound.play() # Joue le son de l'explosion du météore
			expl = Explosion(hit.rect.center, 'lg') # Joue l'animation de l'explosion
			ship_sprites.add(expl)
			new_meteor()

			
		if ship.alive():
			hits = pygame.sprite.spritecollide(ship, meteors, True, pygame.sprite.collide_circle) #Test les collisions entre le vaisseau et les météores. Si collision, météore disparait.
		for hit in hits:
			expl = Explosion(hit.rect.center, 'sm') # Joue le son de l'explosion du météore
			ship_sprites.add(expl) # Joue l'animation de l'explosion
			new_meteor()
			ship.life -= 25 #baisse la vie de 25
			if ship.life == 0: # Si la vie est à 0, le vaisseau explose, et le sprite disparait
				death_explosion = Explosion(ship.rect.center, 'ship')
				ship_sprites.add(death_explosion)
				ship.kill() 

		if not ship.alive() and not death_explosion.alive(): #Quand l'animation de l'explosion est terminée, affiche l'écran du game over et arrête la musique
			ship_continuer=0
			restart=1
			pygame.mixer.music.stop()
			

		hits = pygame.sprite.groupcollide(meteors, mega_bullets, True, False) #Similaire avec les bullets
		for hit in hits:
			expl = Explosion(hit.rect.center, 'lg')
			ship_sprites.add(expl)
			explosion2_sound.play()
			new_meteor()

		hits = pygame.sprite.groupcollide(meteors, lasers, True, False)
		for hit in hits:
			expl = Explosion(hit.rect.center, 'lg')
			ship_sprites.add(expl)
			explosion2_sound.play()
			new_meteor()	
		
		


		draw_life_bar(screen, 5, HAUTEUR-15,ship.life)	#Dessine la barre d'HP
		screen.fill(SPACE_BLUE) #Remplis le fond d'écran de bleu
		meteors.update() #Raffraichit les sprites, puis les affiche
		ship_sprites.update()
		ship_sprite.update()
		meteors.draw(screen)
		ship_sprites.draw(screen)
		ship_sprite.draw(screen)
		time(screen, str(sec), 18, LARGEUR/2, HAUTEUR/10) #Affiche le nombre de secondes passée
		draw_life_bar(screen, 5, HAUTEUR-15,ship.life)
		pygame.display.flip()


	while restart: #Fenetre du game over exactement sur le même principe que l'accueil
		for event in pygame.event.get():	#Attente des événements
			if event.type == QUIT:
				infinite = 0
			if event.type == KEYDOWN :
				if event.key == K_ESCAPE :
					infinite = 0
			if event.type == MOUSEBUTTONDOWN:    #si on clique gauche
				if event.button == 1:	
					if event.pos[0]>= persoR_x and event.pos[0]<= persoR_x2 and event.pos[1]>= persoR_y and event.pos[1]<= persoR_y2 :   #si on clique sur la fenêtre du restart
																	if pacpac:
																		pac_continuer = 1
																		restart = 0
																	if shipship:
																		ship_continuer = 1
																		restart = 0
					if event.pos[0]>= persoQ_x and event.pos[0]<= persoQ_x2 and event.pos[1]>= persoQ_y and event.pos[1]<= persoQ_y2 :   
																	acc_continuer = 1
																	restart = 0
					
			if event.type == MOUSEMOTION: #Si mouvement de souris		
					if event.pos[0]>= persoR_x and event.pos[0]<= persoR_x2 and event.pos[1]>= persoR_y and event.pos[1]<= persoR_y2 : #si souris passe sur fenêtre pacman
																	persoR = pygame.image.load("Restart2.png").convert_alpha()
					else :
						persoR = pygame.image.load("Restart.png").convert_alpha()
					if event.pos[0]>= persoQ_x and event.pos[0]<= persoQ_x2 and event.pos[1]>= persoQ_y and event.pos[1]<= persoQ_y2 :
																	persoQ = pygame.image.load("Quitter2.png").convert_alpha()		
					else :

						persoQ = pygame.image.load("Quitter.png").convert_alpha()
		#Re-collage	
		screen.blit(persoR, (persoR_x, persoR_y))
		screen.blit(persoQ, (persoQ_x, persoQ_y))
		
		#Rafraichissement
		pygame.display.flip()
		

	

pygame.quit()      
