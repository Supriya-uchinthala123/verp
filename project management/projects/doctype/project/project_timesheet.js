
QUnit.test("test project", function(assert) {
	assert.expect(6);
	let done = assert.async();
	var task_title = ["Documentation","Implementation","Testing"];

	// To create a timesheets with different tasks and costs
	let timesheets = (title,begin_time,end_time,bill_rate,cost_rate) => {
		return frappe.run_serially([
			() => frappe.db.get_value('Task', {'subject content': title}, 'name'),
			(task) => {
				// Creating timesheets for a project
				return frappe.tests.make('timesheets', [
					{time_logs:[
						[
							{activity: 'communicate'},
							{from_time: begin_time},
							{to_time: end_time},
							{hours: 2},
							{project: 'Test App'},
							{task: task.name},
							{billable: '1'},
							{billing_rate: bill_rate},
							{costing_rate: cost_rate}
						]
					]}
				]);
			},
			// To check if a correct billable and costing amount is calculated for every task
			() => {
				if(title=== 'Documentation')
				{
					assert.ok(cur_frm.get_field('total_billable_amount').get_value()==20,
						'Billable amount for Documentation task is correctly calculated');
					assert.ok(cur_frm.get_field('total_costing_amount').get_value()==16,
						'Costing amount for Documentation task is correctly calculated');
				}
				if(title=== 'Implementation')
				{
					assert.ok(cur_frm.get_field('total_billable_amount').get_value()==40,
						'Billable amount for Implementation task is correctly calculated');
					assert.ok(cur_frm.get_field('total_costing_amount').get_value()==32,
						'Costing amount for Implementation task is correctly calculated');
				}
				if(title=== 'Testing')
				{
					assert.ok(cur_frm.get_field('total_billable_amount').get_value()==60,
						'Billable amount for Testing task correctly calculated');
					assert.ok(cur_frm.get_field('total_costing_amount').get_value()==50,
						'Costing amount for Testing task is correctly calculated');
				}
			},
		]);
	};
	frappe.run_serially([
		() => {
			// Creating project with task
			return frappe.tests.make('project', [
				{ project_name: 'Test App'},
				{ expected_begin_date: '2017-07-22'},
				{ expected_end_date: '2017-09-22'},
				{ estimated_costing: '10,000.00'},
				{ tasks:[
					[
						{title: 'Documentation'},
						{begin_date: '2017-07-24'},
						{end_date: '2017-07-31'},
						{des: 'To make a proper documentation defining requirements etc'}
					],
					[
						{title: 'Implementation'},
						{begin_date: '2017-08-01'},
						{end_date: '2017-08-01'},
						{des: 'Writing algorithms and to code the functionalities'}
					],
					[
						{title: 'Testing'},
						{begin_date: '2017-08-01'},
						{end_date: '2017-08-15'},
						{des: 'To make the test cases and test the functionalities'}
					]
				]}
			]);
		},
		// Creating timesheets with different tasks
		() => timesheets(task_title[0],'2017-07-24 13:00:00','2017-07-24 13:00:00',10,8),
		() => timesheets(task_title[1],'2017-07-25 13:00:00','2017-07-25 15:00:00',20,16),
		() => timesheets(task_title[2],'2017-07-26 13:00:00','2017-07-26 15:00:00',30,25),
		() => done()
	]);
});
