from django.shortcuts import render
from users.models import User
from poll.models import AllCandidateGet, AllPostsGet
import pandas as pd
from zipfile import ZipFile 
import os
from django.http import HttpResponse, FileResponse


def get_all_file_paths(directory): 
    file_paths = [] 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            if ".xlsx" in filename:
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
    return file_paths


def viewresults(request):
    context = {}
    context['candidates'] = AllCandidateGet()
    context['posts'] = AllPostsGet()
    return render(request, 'results.html', context)


def save_excel(request):
    AllCandidates = AllCandidateGet()
    df  = pd.DataFrame(columns = ['admission_no', 'name', 'position', 'vote'])
    for i in AllCandidates:
        df.loc[len(df)] = AllCandidates[i]
    df.rename(columns={'admission_no': 'Admission No', 'name': 'Name', 'position': 'Position', 'vote': 'Number Of Votes'}, inplace=True)
    df.to_excel("Results.xlsx")

    PostWise = AllPostsGet()
    for i in PostWise:
        df  = pd.DataFrame(columns = ['admission_no', 'name', 'vote'])
        for j in PostWise[i]:
            df.loc[len(df)] = PostWise[i][j]
        df.rename(columns={'admission_no': 'Admission No', 'name': 'Name', 'vote': 'Number Of Votes'}, inplace=True)
        df.to_excel(i + ".xlsx")

    file_paths = get_all_file_paths(os.getcwd())
    with ZipFile('ElectionResult2020.zip','w') as zip: 
        for file in file_paths:
            zip.write(file)
            os.remove(file)

    zip_file = open('ElectionResult2020.zip', 'rb')
    return FileResponse(zip_file)