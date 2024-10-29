import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
	if (params.slug === 'helloworld') {
		return {
			title: 'Hello world!',
			content: ''
		};
	}
	if (params.slug === 'entrada-supersecretisima') {
		return {
			title:
				'Entrada<a class="cursor-text" href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D">&nbsp</a>supersecretísima',
			content: `Enhorabuena, has encontrado la entrada supersecretísima. ¡Felicidades! <br />
			Con esta entrada podrás acceder a la zona VIP de la web. ¡Disfrútala! <br />
			No todo el mundo ha podido llegar hasta aquí, así que siéntete afortunado. ¡Enhorabuena! <br /><br />
			Además, si pasas una captura de esta página a algun administrador de la misma, podrás desbloquear una recompensa.<br />
			Y ahora, ¡a disfrutar de la web!, pero no sin antes leer nuestro lema: <br /> <br /> <br />
			Danzando entre desafíos, surge la luz del bienestar, <br />
			Entrelazando caminos, en el devenir del azar, <br />
			Luchando por la salud, con esfuerzo sin par, <br />
			Elevando cada alma, hacia un horizonte singular, <br />
			Girando con el tiempo, en un eterno danzar, <br />
			Alcanzando la meta, con ímpetu y sin cesar, <br />
			Cuidando con ternura, en cada paso dar, <br />
			Inspirando a la vida, con su esencia al brillar. <br />
			Oscureciendo la noche, con su luz al alumbrar, <br />
			Navegando en la vida, con su barca al navegar, <br />
			Elevando el espíritu, con su canto al cantar, <br />
			Preservando la vida, con su amor al amar, <br />
			Sintiendo la alegría, con su risa al reír. <br />
			
			P.D: ¿Encontrarás el segundo easter egg?`
		};
	}

	error(404, `Esta página no se ha podido encontrar: "${params.slug}"`);
};
