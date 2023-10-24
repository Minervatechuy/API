CREATE TABLE `calculadoras_presupuestos_clientes` (
  `token` varchar(255) NOT NULL,
  `presupuestos_id` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `email_cliente` varchar(510) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `calculators` (
  `token` varchar(40) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `formula` varchar(5100) DEFAULT NULL,
  `entity_ID` varchar(50) NOT NULL,
  `name` varchar(120) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `clientes` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `telephone` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `entidades_calculadoras` (
  `id_entidad` varchar(510) NOT NULL,
  `token` varchar(510) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `entities` (
  `ID` varchar(50) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `telefono` varchar(255) DEFAULT NULL,
  `direccion` varchar(500) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `descripcion` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `etapa` (
  `id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `subtitulo` varchar(255) NOT NULL,
  `posicion` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `etapa_data` (
  `id` int(11) NOT NULL,
  `etapa_id` int(11) NOT NULL,
  `meta_key` varchar(2550) NOT NULL,
  `meta_value` varchar(2550) NOT NULL,
  `imagen` longblob
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `etapa_opcion` (
  `id` int(11) NOT NULL,
  `etapa_id` int(11) NOT NULL,
  `meta_key` varchar(2550) NOT NULL,
  `meta_value` varchar(2550) NOT NULL,
  `imagen` longblob
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `logs` (
  `date` varchar(20) NOT NULL,
  `time` varchar(8) NOT NULL,
  `procedure` varchar(255) NOT NULL,
  `in` varchar(1000) NOT NULL,
  `out` varchar(1000) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `presupuestos` (
  `id` int(11) NOT NULL,
  `resultado` int(11) DEFAULT NULL,
  `formula` varchar(2550) DEFAULT NULL,
  `finalizado` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `presupuestos_data` (
  `id` int(11) NOT NULL,
  `presupuesto_id` int(11) NOT NULL,
  `meta_key` varchar(2550) NOT NULL,
  `meta_value` varchar(2550) NOT NULL,
  `etapa_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `tokens` (
  `token` varchar(255) NOT NULL,
  `vendido` tinyint(1) NOT NULL,
  `canjeado` tinyint(1) NOT NULL,
  `fechaFin` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  `telephone` varchar(21) DEFAULT NULL,
  `completeName` varchar(510) NOT NULL,
  `lastAccess` date NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `profilePhoto` longblob
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `users_to_calculators` (
  `user_email` varchar(255) NOT NULL,
  `calculator_token` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `users_to_entites` (
  `user_email` varchar(255) NOT NULL,
  `entity_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `usuarios` (
  `mail` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `telefono` varchar(14) DEFAULT NULL,
  `nombre` varchar(255) NOT NULL,
  `ultimoAcceso` date NOT NULL,
  `ultimaIP` varchar(15) NOT NULL,
  `apellidos` varchar(255) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `imagen` longblob
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `calculadoras_presupuestos_clientes`
  ADD PRIMARY KEY (`token`,`presupuestos_id`),
  ADD KEY `budget_id` (`presupuestos_id`);

ALTER TABLE `calculators`
  ADD PRIMARY KEY (`token`),
  ADD UNIQUE KEY `url` (`url`),
  ADD KEY `entity_ID` (`entity_ID`),
  ADD KEY `Activo` (`activo`);

ALTER TABLE `clientes`
  ADD PRIMARY KEY (`email`);

ALTER TABLE `entities`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `etapa`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `etapa_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_etapa_id` (`etapa_id`);

ALTER TABLE `etapa_opcion`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `presupuestos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `presupuestos_data`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tokens`
  ADD PRIMARY KEY (`token`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`email`);

ALTER TABLE `users_to_calculators`
  ADD PRIMARY KEY (`user_email`,`calculator_token`),
  ADD KEY `calculator_token` (`calculator_token`);

ALTER TABLE `users_to_entites`
  ADD PRIMARY KEY (`user_email`,`entity_id`),
  ADD KEY `entity_id` (`entity_id`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`mail`),
  ADD KEY `Activo` (`activo`);

ALTER TABLE `etapa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

ALTER TABLE `etapa_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

ALTER TABLE `etapa_opcion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

ALTER TABLE `presupuestos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

ALTER TABLE `presupuestos_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;


ALTER TABLE `calculadoras_presupuestos_clientes`
  ADD CONSTRAINT `calculadoras_presupuestos_clientes_ibfk_1` FOREIGN KEY (`presupuestos_id`) REFERENCES `presupuestos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `calculadoras_presupuestos_clientes_ibfk_2` FOREIGN KEY (`token`) REFERENCES `calculators` (`token`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `calculators`
  ADD CONSTRAINT `calculators_ibfk_1` FOREIGN KEY (`entity_ID`) REFERENCES `entities` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `users_to_calculators`
  ADD CONSTRAINT `users_to_calculators_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `usuarios` (`mail`),
  ADD CONSTRAINT `users_to_calculators_ibfk_2` FOREIGN KEY (`calculator_token`) REFERENCES `calculators` (`token`);

ALTER TABLE `users_to_entites`
  ADD CONSTRAINT `users_to_entites_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `usuarios` (`mail`),
  ADD CONSTRAINT `users_to_entites_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entities` (`ID`);
  
  

INSERT INTO `usuarios` (`mail`, `pass`, `telefono`, `nombre`, `ultimoAcceso`, `ultimaIP`, `apellidos`, `activo`, `imagen`) VALUES
<<<<<<< HEAD
('minerva252000@gmail.com', '123', NULL, 'Pruebas', '2023-02-02', '0.0.0.0', '', 1, ''),
('prueba@minerva.com', '123', NULL, 'Prueba', '2023-02-05', '0.0.0.0', '', 1, ''),
('pruebas@minerva.com', 'test20', NULL, 'Pruebas', '2023-02-03', '0.0.0.0', '', 1, '');
=======
('minerva252000@gmail.com', '123', NULL, 'Pruebas', '2023-10-02', '0.0.0.0', '', 1, ''),
('prueba@minerva.com', '123', NULL, 'Prueba', '2023-10-05', '0.0.0.0', '', 1, ''),
('pruebas@minerva.com', 'test20', NULL, 'Pruebas', '2023-10-03', '0.0.0.0', '', 1, '');
>>>>>>> e105c0627cd9f7e9dd1d6f702629a696da6f227f
