document.addEventListener('DOMContentLoaded', function () {
  const timetableData = JSON.parse('{{ emploi_du_temps|safe }}');

  // Vérifier si timetableData contient des données
  if (timetableData && Array.isArray(timetableData) && timetableData.length > 0) {
      // Map des jours en français pour FullCalendar (0 = Dimanche)
      const dayMapping = {
        LUNDI: 1,
        MARDI: 2,
        MERCE: 3,
        JEUDI: 4,
        VENDR: 5,
      };

      // Convertir les données en événements pour FullCalendar
      const events = timetableData.map(event => {
        const day = dayMapping[event.jour];
        if (day === undefined) return null; // Ignorer si le jour est invalide

        // Construire la date actuelle pour les heures (par défaut, semaine courante)
        const today = new Date();
        const eventDate = new Date(today.setDate(today.getDate() - today.getDay() + day));

        // Fusionner date et heures de début/fin
        const startDate = new Date(eventDate);
        startDate.setHours(parseInt(event.debut.split(':')[0]));
        startDate.setMinutes(parseInt(event.debut.split(':')[1]));

        const endDate = new Date(eventDate);
        endDate.setHours(parseInt(event.fin.split(':')[0]));
        endDate.setMinutes(parseInt(event.fin.split(':')[1]));

        return {
          title: `${event.uv} (${event.type}, ${event.salle})`,
          start: startDate.toISOString(),
          end: endDate.toISOString(),
        };
      }).filter(event => event !== null); // Supprimer les jours invalides

      // Calculer l'heure de fin maximale (la fin du dernier cours)
      const latestEndTime = events.reduce((latest, event) => {
        const eventEnd = new Date(event.end);
        return eventEnd > latest ? eventEnd : latest;
      }, new Date(0)); // Initialiser avec une date très ancienne

      // Formater l'heure de fin maximale en 'HH:mm:ss'
      const latestEndTimeString = latestEndTime.toISOString().substring(11, 19);

      const calendarEl = document.getElementById('calendar');
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'fr',
        firstDay: 1, // Lundi comme premier jour
        hiddenDays: [0, 6], // Cache dimanche (0) et samedi (6)
        slotMinTime: '08:00:00', // Début de la journée à 8h
        slotMaxTime: latestEndTimeString, // Fin de la journée à l'heure de fin du dernier cours
        events: events,
        allDaySlot: false,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'timeGridWeek,timeGridDay',
        },
      });

      calendar.render();
  } else {
      document.getElementById("edt").innerHTML = "Aucun emploi du temps pour le moment.";
  }
});
