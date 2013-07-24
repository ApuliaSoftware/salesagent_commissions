<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>

	<h1 class="centered">RIEPILOGO PROVVIGIONI</h1>

	<table class="table_data">
		<tr>
			<td class="centered w35">AGENTE</td>
			<td class="centered w10">NUMERO</td>
			<td class="centered w10">DATA</td>
			<td class="centered w35">CLIENTE</td>
			<td class="centered w10">PROVVIGIONE</td>
		</tr>
	<% tot = 0.0 %>
	% for record in objects:
		<tr>
			<td>${record.salesagent_id.name}</td>
			<td>${record.number or ''}</td>
			<td>${record.date_invoice}</td>
			<td>${record.partner_id.name}</td>
			<td>${record.commission}</td>
		</tr>
		<% tot += record.commission %>
	%endfor
		<tr>
			<td colspan="4">&nbsp;</td>
			<td class="centered"><b>${tot}</b></td>
		</tr>
	</table>
	
	

</body>
</html>
