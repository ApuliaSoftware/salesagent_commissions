<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>

	<h1 class="centered">RIEPILOGO PROVVIGIONI</h1>

	<table class="table_data_no_board">
		<tr>
			<td class="centered w30">AGENTE</td>
			<td class="centered w10">NUMERO</td>
			<td class="centered w10">DATA</td>
			<td class="centered w30">CLIENTE</td>
			<td class="centered w10">PROVV.</td>
			<td class="centered w10">IMP.</td>
		</tr>
	<% tot_commission = 0.0 %>
	<% tot_untaxed = 0.0 %>
	% for record in objects:
		<tr>
			<td>${record.salesagent_id.name}</td>
			<td>${record.number or ''}</td>
			<td>${record.date_invoice}</td>
			<td>${record.partner_id.name}</td>
			<td>${record.commission}</td>
			<td>${record.amount_untaxed}</td>
		</tr>
		<% tot_commission += record.commission %>
		<% tot_untaxed += record.amount_untaxed %>
	%endfor
		<tr>
			<td colspan="4">&nbsp;</td>
			<td class="centered"><b>${tot_commission}</b></td>
			<td class="centered"><b>${tot_untaxed}</b></td>
		</tr>
	</table>
	
	

</body>
</html>
