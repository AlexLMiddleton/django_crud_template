import os
import shutil

#########################################

# Template string formatters

nl = '\n'
tab = '\t'

#########################################

# User Input

# Ask the user to input the name of their default project
project_name = input("Enter your project's name: ")

# Ask the user to input the name of their default app
app_name = input("Enter your app's name: ")

# # Ask the user to input the number of models they'll want to create
models_input = input('Enter the total number of models you wish to create: ')

# # Convert the number the user inputted (a string) to an INT for looping purposes
models_number = int(models_input)

#########################################

# Functions

# # Loop through folders searching for files that start with a particular string, and then replace it with a user-defined string
def rename_folder(old_folder_name, replaced_name):
    for entry in os.scandir('./'):
        if entry.name.startswith(old_folder_name):
            os.rename(os.path.join('./', entry.name), os.path.join('./', entry.name.replace(old_folder_name, replaced_name.lower())))

# # Scan all files in a given folder, searching for a particular hardcoded string, and replace it with a user-defined string
def scan_files_and_replace(folder_name, old_file_name, replaced_file_name):
    for entry in os.scandir(f'./{folder_name}'):
        if entry.name.endswith('.py'):
            with open(entry) as file:
                s = file.read()
            replaced = s.replace(old_file_name, replaced_file_name)
            if entry.name.endswith('.py'):
                with open(entry, 'w') as f:
                    f.write(replaced)

#########################################

# PROJECT

# # Replace the template project name with the user-defined name in the manage.py file
with open('./manage.py', 'r') as manager:
    manage = manager.read()
    manage = manage.replace('django_template_project', project_name)
with open('./manage.py', 'w') as manager:
    manager.write(manage)

# # Scan the current directory's folders for a 'django_template_project' folder.  Replace the name with the user's Project Name input.
rename_folder('django_template_project', project_name)

# # Scan the files within the app folder and replace "django_template_project" with the user's Project Name input.
scan_files_and_replace(project_name, 'django_template_project', project_name)

#########################################

# APP

# Change the app name in the {project_name}/settings.py file
with open(f'./{project_name}/settings.py', 'r') as settings_list:
    manage = settings_list.read()
    manage = manage.replace('django_template_app', app_name)
with open(f'./{project_name}/settings.py', 'w') as settings_list:
    settings_list.write(manage)

# Scan the current directory's folders for a 'django_template_app' folder.  Replace the name with the user's App Name input.
rename_folder('django_template_app', app_name)

# Scan the files within the Projects folder and replace "django_template_app" with the user's App Name input.
scan_files_and_replace(project_name, 'django_template_app', app_name)

# Scan the files within the App folder and replaced "django_template_app" with the user's App Name input.
scan_files_and_replace(app_name, 'django_template_app', app_name)

#########################################

# MODEL

# Open the base.html file and change the Project Title to the name of our project
with open(f'./{app_name}/templates/base.html', 'r') as current:
    read_entry = current.read()
    replace_text = read_entry.replace('ProjectTitle', f'{project_name}')
with open(f'./{app_name}/templates/base.html', 'w') as current:
    current.write(replace_text)

os.mkdir(f'./{app_name}/templates/{app_name}')

urls_list = []

for x in range(models_number):
    # Ask the user for the name for each of the models, which will then be used to build Models, URLs, Forms, Views, HTML templates, etc.
    model_name = input('Enter the name for model ' + str(x + 1) + ': ')

    # Build a barebones model template for each model name they enter (comes with ID primary key and a generic CharField)
    with open(f'./{app_name}/models.py', 'a+') as modelFile:
        modelFile.write(f'{nl}class {model_name}(models.Model):{nl}{tab}id = models.AutoField(primary_key=True){nl}{tab}{model_name.lower()}_name = models.CharField(max_length = 30)')

    # Create the views for each model
    with open(f'./{app_name}/views.py', 'a+') as viewFile:
        viewFile.write(f'{nl}{nl}class {model_name}ListView(ListView):{nl}{tab}model={model_name}')
        viewFile.write(f'{nl}{nl}class {model_name}DetailView(DetailView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_detail.html\'')
        viewFile.write(f'{nl}{nl}class {model_name}CreateView(CreateView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_add.html\'{nl}{tab}fields=\'__all__\'{nl}{tab}success_url=reverse_lazy(\'' + model_name.lower() + '-list\')')
        viewFile.write(f'{nl}{nl}class {model_name}UpdateView(UpdateView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_edit.html\'{nl}{tab}fields=\'__all__\'{nl}{tab}success_url=reverse_lazy(\'' + model_name.lower() + '-list\')')
        viewFile.write(f'{nl}{nl}class {model_name}DeleteView(DeleteView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_delete.html\'{nl}{tab}success_url=reverse_lazy(\'{model_name.lower()}-list\')')
    
    # Create the URL patterns for each model
    with open(f'./{app_name}/urls.py', 'a') as urls:
        urls.seek(urls.tell() - 1, os.SEEK_SET)
        urls.truncate()
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/\', {model_name}ListView.as_view(), name=\'{model_name.lower()}-list\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/<int:pk>/\', {model_name}DetailView.as_view(), name=\'{model_name.lower()}-detail\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/new/\', {model_name}CreateView.as_view(), name=\'{model_name.lower()}-create\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/edit/<int:pk>/\', {model_name}UpdateView.as_view(), name=\'{model_name.lower()}-edit\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/delete/<int:pk>/\', {model_name}DeleteView.as_view(), name=\'{model_name.lower()}-delete\'),{nl}')
        urls.write(']')
    
    # Build out a form for each model
    with open(f'./{app_name}/forms.py', 'a') as forms:
        forms.write(f'{nl}class {model_name}Form(ModelForm):{nl}{tab}class Meta:{nl}{tab}{tab}model = {model_name}{nl}{tab}{tab}exclude = []{nl}{tab}{tab}fields = \'__all__\'{nl}')
    
    # Register each model in the admin file
    with open(f'./{app_name}/admin.py', 'a') as adminRegistry:
        adminRegistry.write(f'{nl}admin.site.register({model_name})')
    
    # Copy the template HTML files, place them in the correct spot to be read, and then rename them to the {model}_<file_ending>.html format
    shutil.copyfile(f'./{app_name}/templates/index.html', f'./{app_name}/templates/{app_name}/{model_name.lower()}_list.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_add.html', f'./{app_name}/templates/{app_name}/{model_name.lower()}_add.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_delete.html', f'./{app_name}/templates/{app_name}/{model_name.lower()}_delete.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_detail.html', f'./{app_name}/templates/{app_name}/{model_name.lower()}_detail.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_edit.html', f'./{app_name}/templates/{app_name}/{model_name.lower()}_edit.html')
    
    # Creating a list of URL links from our models
    urls_list.append(f'<a class="dropdown-item" href="{{% url "{model_name.lower()}-list" %}}">{model_name}</a>')
    s = nl.join(urls_list)

    # Scan the templates directory.  When you find an instance of "newmodel", "ModelTitle", or "ProjectTitle", replace them with the appropriate user-input values
    for entry in os.scandir(f'./{app_name}/templates/{app_name}'):
        with open(entry, 'r') as current:
            read_entry = current.read()
            replace_text = read_entry.replace('newmodel', model_name.lower()).replace('ModelTitle', model_name).replace('template_field_name', f'{model_name.lower()}_name')
        with open(entry, 'w') as current:
            current.write(replace_text)

    # On the very last loop, searches through every folder in the templates directory and replaces "placeholderText" with the model names/URLs to populate the dropdown menu
    if x == models_number -1:
        for entry in os.scandir(f'./{app_name}/templates/{app_name}'):
            with open(entry, 'r') as current:
                read_entry = current.read()
                replace_text = read_entry.replace("placeholderText", s)
            with open(entry, 'w') as current:
                current.write(replace_text)



# Do a precautionary migrate, then make migrations, and then push those migrations up
os.system('python manage.py migrate')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')