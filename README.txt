Introduction :

	Le but �tant d'impl�menter un "traducteur" de SPJRUD vers sqlite3 en testant si les requetes �taient correctes,
il fallait donc d�finir des classes repr�sentant les diff�rentes expressions de SPJRUD, a savoir le Select, le Project, le Join, le Rename, l'Union et la Difference.
Le Select �tant toujours attribut=constante ou attribut=attribut, il n'�tait pas n�c�ssaire de creer un Eq() dans l'ast.
Cela posait un probleme, il y avait 3 nouvelles variables(classes) : Attribut, Constante et Relation.
Un traducteur signifiait une fonction traduction() et une verification n�c�ssitait une fonction v�rification().


Choix d'impl�mentation : 

	N'ayant pas beacoup d'ann�es de pratique sur le language python, je doute avoir utilis� tous les raccourcis possibles pour terminer l'impl�mentation, le peu de
connaissances que j'ai sur ce language me viens du cours de premiere bac et d'internet.

J'ai utilis� une classe Table pour ne pas devoir chercher dans la base de donn�e et pour afficher les tables � ma convenance.
Pour cela, la table contient le nom de la table, le nom des attributs, le type des attributs et le tuples de la table.
Elle contient �galement une fonction display() qui l'affiche.

Une classe Expr qui contient la table sur laquelle l'expression utilis�e, une expression qui correspond a la requete SPJRUD et une traduction qui correspond a la 
requete SQL.
Une fonction validation qui prend en argument les tables de la base de donn�es pour effectuer les verifications et une fonction display() pour afficher la table de
la requete.

Les classes Attr, Rel et Const qui sont les atomes de l'ast et les classes Select, Project, Join, Rename, Union et Diff qui sont les noeuds de l'ast.
Rel et les noeuds qui h�ritent de Expr, les 2 autres non �tant donn� qu'elle ne repr�sentent pas de table.


Comment utiliser ? :

	La syntaxe est la suivante : 

		Attr('a') : a le nom de l'attribut | exemple : Attr('A1')
		Const(a) : a la valeur de la constante | exemple : Const(3)/Const('Asteroide')
		Rel('a') : a le nom de la relation | exemple : Rel('R1')

		Select(Attr(), Const(), Expr()) : Expr() une autre requete SPJRUD | exemple : Select(Attr('A1'),  Const('Asteroide'), Rel('E1'))
		Select(Attr(), Attr(), Expr()) : Expr() une autre repuete SPJRUD | exemple : Select(Attr('A1'), Attr('A2'), Rel('R1'))

		Project([], Expr()) : [] les attributs ; [Attr('A1'), Attr('A2')] | exemple : Project([Attr('A2'), Attr('A5')], Rel('R1'))

		Join(Expr(), Expr()) : Expr() une autre repuete SPJRUD | exemple : Join(Rel('E1'), Rel('A12'))

		Rename([A], [B], Expr()) : [A] : les attributs ; [Attr('A1'), Attr('A3')],  [B] : les constantes ; [Const('S2'), Const('S4')] | exemple : Rename([Attr('A1'), Attr('A2')], [Const('Z1'), Const('Z2')], Rel('R1'))

		Union(Expr(), Expr()) : Expr() une autre repuete SPJRUD | exemple : Union(Rel('A1'), Rel('A2'))

		Diff(Expr(), Expr()) : Expr() une autre repuete SPJRUD | exemple : Diff(Rel('R1'), Rel('R2'))

	Appliquer une requete SPJRUD sur une base de donn�es :

		SPJRUD2sqlite3(path, requete) : path : le chemin jusque le fichier base de donn�es, requete : la requete SPJRUD  | exemple : SPJRUD2sqlite3('myDB.db', Select(Attr('A1'), Const('Charles'), Rel('R1')))


	Lancer les Tests : 

		tests()